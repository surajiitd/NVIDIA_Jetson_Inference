import torch
import torch.backends.cudnn as cudnn

import os, sys
import argparse
import numpy as np
from tqdm import tqdm
import time
import cv2
from utils import post_process_depth, flip_lr, compute_errors
from networks.NewCRFDepth import NewCRFDepth
#from sklearn.linear_model import HuberRegressor



def convert_arg_line_to_args(arg_line):
    for arg in arg_line.split():
        if not arg.strip():
            continue
        yield arg


parser = argparse.ArgumentParser(description='NeWCRFs PyTorch implementation.', fromfile_prefix_chars='@')
parser.convert_arg_line_to_args = convert_arg_line_to_args

parser.add_argument('--model_name',                type=str,   help='model name', default='newcrfs')
parser.add_argument('--encoder',                   type=str,   help='type of encoder, base07, large07', default='large07')
parser.add_argument('--checkpoint_path',           type=str,   help='path to a checkpoint to load', default='')

# Dataset
parser.add_argument('--dataset',                   type=str,   help='dataset to train on, kitti or nyu', default='nyu')
parser.add_argument('--input_height',              type=int,   help='input height', default=480)
parser.add_argument('--input_width',               type=int,   help='input width',  default=640)
parser.add_argument('--max_depth',                 type=float, help='maximum depth in estimation', default=10)

# Preprocessing
parser.add_argument('--do_random_rotate',                      help='if set, will perform random rotation for augmentation', action='store_true')
parser.add_argument('--degree',                    type=float, help='random rotation maximum degree', default=2.5)
parser.add_argument('--do_kb_crop',                            help='if set, crop input images as kitti benchmark images', action='store_true')
parser.add_argument('--use_right',                             help='if set, will randomly use right images when train on KITTI', action='store_true')

# Eval
parser.add_argument('--data_path_eval',            type=str,   help='path to the data for evaluation', required=False)
parser.add_argument('--gt_path_eval',              type=str,   help='path to the groundtruth data for evaluation', required=False)
parser.add_argument('--filenames_file_eval',       type=str,   help='path to the filenames text file for evaluation', required=False)
parser.add_argument('--min_depth_eval',            type=float, help='minimum depth for evaluation', default=1e-3)
parser.add_argument('--max_depth_eval',            type=float, help='maximum depth for evaluation', default=80)
parser.add_argument('--eigen_crop',                            help='if set, crops according to Eigen NIPS14', action='store_true')
parser.add_argument('--garg_crop',                             help='if set, crops according to Garg  ECCV16', action='store_true')
parser.add_argument('--gray', help='Use gray images for testing', action='store_true')


if sys.argv.__len__() == 2:
    arg_filename_with_prefix = '@' + sys.argv[1]
    args = parser.parse_args([arg_filename_with_prefix])
else:
    args = parser.parse_args()

if args.dataset == 'kitti' or args.dataset == 'nyu' or \
    args.dataset == '12scenes' or args.dataset == 'iitd'\
    or args.dataset == 'eth3d':
    from dataloaders.dataloader import NewDataLoader
elif args.dataset == 'kittipred':
    from dataloaders.dataloader_kittipred import NewDataLoader

def get_mono_ratio(prediction, target, min_depth, max_depth):
    """Returns the median scaling factor from gt_depth and pred_depth,
        Tells by what scale factor you should scale up(multipy) your pred_depth.
    """
    mask = np.logical_and(target>min_depth , target<max_depth)
    scale = np.median(target[mask]) / np.median(prediction[mask])
    return prediction*scale

def get_scale_shift(prediction, target,  min_depth, max_depth):
    """Returns the median scaling factor from gt_depth and pred_depth,
        Tells by what scale factor you should scale up(multipy) your pred_depth.
    """
    mask = np.logical_and(target>min_depth , target<max_depth)
    scale = np.median(target[mask]) / np.median(prediction[mask])
    return scale, 0.0


def eval(model, dataloader_eval, post_process=False):
    eval_measures = torch.zeros(10).cuda()
    valid_index = 0
    top_abs_rel_indices = []
    top_rmse_indices = []
    start_time = time.time()
    for txt_idx, eval_sample_batched in enumerate(dataloader_eval.data):
        #print("index = ",txt_idx)
        with torch.no_grad():
            image = torch.autograd.Variable(eval_sample_batched['image'].cuda())
            gt_depth = eval_sample_batched['depth']
            has_valid_depth = eval_sample_batched['has_valid_depth']
            if not has_valid_depth:
                # print('Invalid depth. continue.')
                continue
            import ipdb; ipdb.set_trace()
            pred_depth = model(image)
            if post_process:
                image_flipped = flip_lr(image)
                pred_depth_flipped = model(image_flipped)
                pred_depth = post_process_depth(pred_depth, pred_depth_flipped)

            pred_depth = pred_depth.cpu().numpy().squeeze()
            gt_depth = gt_depth.cpu().numpy().squeeze()
            img = eval_sample_batched['unnormalized_image'].cpu().numpy().squeeze().transpose((1,2,0))
          
        # if args.dataset == "kitti" or args.dataset=="nyu":
        pred_depth[pred_depth < args.min_depth_eval] = args.min_depth_eval
        pred_depth[pred_depth > args.max_depth_eval] = args.max_depth_eval
        pred_depth[np.isinf(pred_depth)] = args.max_depth_eval
        pred_depth[np.isnan(pred_depth)] = args.min_depth_eval
        
        #pred_depth = get_mono_ratio(pred_depth, gt_depth, min_depth=args.min_depth_eval, max_depth=args.max_depth_eval )
        scale, shift = get_scale_shift(pred_depth, gt_depth, min_depth=args.min_depth_eval, max_depth=args.max_depth_eval )
        #print("scale = ",scale)
        pred_depth = pred_depth*scale+shift
        
        """ uncomment later
        if args.dataset=="kitti" or args.dataset=='eth3d' or args.dataset=="nyu" :
            valid_mask = np.logical_and(gt_depth > args.min_depth_eval, gt_depth < args.max_depth_eval)
        elif args.dataset == "iitd":
            valid_mask = np.logical_and(gt_depth > args.min_depth_eval, gt_depth < 6.0)
        eval_mask = np.ones(valid_mask.shape)

        if args.garg_crop or args.eigen_crop:
            gt_height, gt_width = gt_depth.shape
            eval_mask = np.zeros(valid_mask.shape)

            if args.garg_crop:
                eval_mask[int(0.40810811 * gt_height):int(0.99189189 * gt_height), int(0.03594771 * gt_width):int(0.96405229 * gt_width)] = 1

            elif args.eigen_crop:
                if args.dataset == 'kitti' or args.dataset=='eth3d':
                    eval_mask[int(0.3324324 * gt_height):int(0.91351351 * gt_height), int(0.0359477 * gt_width):int(0.96405229 * gt_width)] = 1
                elif args.dataset == 'nyu':
                    eval_mask[45:471, 41:601] = 1

            valid_mask = np.logical_and(valid_mask, eval_mask)

        measures = compute_errors(gt_depth[valid_mask], pred_depth[valid_mask])
        
        #print(measures)
        
        # top_abs_rel_indices.append([measures[1],valid_index,txt_idx])
        # top_rmse_indices.append([measures[3], valid_index,txt_idx])
        valid_index += 1
        eval_measures[:9] += torch.tensor(measures).cuda()
        eval_measures[9] += 1
        
        # show images, gt_depth and pred_depth.
        img = (img*255).astype(np.uint8)
        img = img[...,::-1]
        # make magma image of gt_depth with 3 channels.
        def _get_colored_depth(depth):
            # Normalize the depth map to a range of 0-255 for better visualization
            depth = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
            # Apply a colormap to the depth map using "magma" or "plasma" as color coding
            colored_depth = cv2.applyColorMap(depth, cv2.COLORMAP_MAGMA)
            return colored_depth
        def print_minmax(arr,desc):
            #visualize depths and uncertainty of any method
            
            print("*" * 60)
            print("***{}***  :".format(desc))
            print("arr.shape = {}".format(arr.shape))
            print("type(arr[0,0] = {}".format(type(arr[0,0])))
            print("np.min = {}".format(np.min(arr)))
            print("np.max = {}".format(np.max(arr)))
            print("np.mean = {}".format(np.mean(arr)))
            print("np.median = {}".format(np.median(arr)))
            #print("arr[200:220,200:220] = \n",arr[200:220,200:220])
            print("arr[0:10,0:10] = \n",arr[0:10,0:10])
            print("*" * 60 + "\n")
        
        # print_minmax(gt_depth,"gt_depth")
        # print_minmax(pred_depth,"pred_depth")
        #cv2.putText(img, 'Image', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


        cv2.putText(img, "Image", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        gt_depth = _get_colored_depth(gt_depth)
        pred_depth = _get_colored_depth(pred_depth)


        #gt_depth = cv2.putText(gt_depth, 'GT Depth', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        #pred_depth = cv2.putText(pred_depth, 'Predicted Depth', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        
        # stack image, gt_depth and pred_depth.
        stacked_img = np.hstack((img, gt_depth, pred_depth))
        cv2.imshow("output", stacked_img)
        #cv2.waitKey(1)
        cv2.waitKey(0)
        """
        


    end_time = time.time()
    print(f"Took {(end_time-start_time):.4f}seconds for {len(dataloader_eval.data)} images!!")
    print(f"For one image = {((end_time-start_time)/len(dataloader_eval.data)):.4f}seconds")
    """
    eval_measures_cpu = eval_measures.cpu()
    cnt = eval_measures_cpu[9].item()
    eval_measures_cpu /= cnt
    print('Computing errors for {} eval samples'.format(int(cnt)), ', post_process: ', post_process)
    print("{:>7}, {:>7}, {:>7}, {:>7}, {:>7}, {:>7}, {:>7}, {:>7}, {:>7}".format('silog', 'abs_rel', 'log10', 'rms','sq_rel', 'log_rms', 'd1', 'd2','d3'))

    for i in range(8):
        print('{:7.4f}, '.format(eval_measures_cpu[i]), end='')
    print('{:7.4f}'.format(eval_measures_cpu[8]))
    return eval_measures_cpu
    """

def main_worker(args):

    # CRF model
    model = NewCRFDepth(version=args.encoder, inv_depth=False, max_depth=args.max_depth, pretrained=None)
    model.train()

    # num_params = sum([np.prod(p.size()) for p in model.parameters()])
    # print("== Total number of parameters: {}".format(num_params))

    # num_params_update = sum([np.prod(p.shape) for p in model.parameters() if p.requires_grad])
    # print("== Total number of learning parameters: {}".format(num_params_update))

    model = torch.nn.DataParallel(model)
    model.cuda()

    print("== Model Initialized")

    if args.checkpoint_path != '':
        if os.path.isfile(args.checkpoint_path):
            print("== Loading checkpoint '{}'".format(args.checkpoint_path))
            checkpoint = torch.load(args.checkpoint_path, map_location='cpu')
            model.load_state_dict(checkpoint['model'])
            print("== Loaded checkpoint '{}'".format(args.checkpoint_path))
            del checkpoint
        else:
            print("== No checkpoint found at '{}'".format(args.checkpoint_path))

    cudnn.benchmark = True

    dataloader_eval = NewDataLoader(args, 'online_eval')

    # ===== Evaluation ======
    model.eval()
    with torch.no_grad():
        eval_measures = eval(model, dataloader_eval, post_process=False)


def main():
    torch.cuda.empty_cache()
    args.distributed = False
    ngpus_per_node = torch.cuda.device_count()
    if ngpus_per_node > 1:
        print("This machine has more than 1 gpu. Please set \'CUDA_VISIBLE_DEVICES=0\'")
        #return -1
    
    main_worker(args)


if __name__ == '__main__':
    main()

from __future__ import absolute_import, division, print_function

import torch
import torch.nn as nn
from torch.autograd import Variable

import os, sys, errno
import argparse
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm

from utils import post_process_depth, flip_lr
from networks.NewCRFDepth import NewCRFDepth


def convert_arg_line_to_args(arg_line):
    for arg in arg_line.split():
        if not arg.strip():
            continue
        yield arg


def print_minmax(arr,desc):
    """visualize depths and uncertainty of any method"""
    
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

parser = argparse.ArgumentParser(description='NeWCRFs PyTorch implementation.', fromfile_prefix_chars='@')
parser.convert_arg_line_to_args = convert_arg_line_to_args

parser.add_argument('--model_name', type=str, help='model name', default='newcrfs')
parser.add_argument('--encoder', type=str, help='type of encoder, base07, large07', default='large07')
parser.add_argument('--data_path_eval', type=str, help='path to the data', required=True)
parser.add_argument('--gt_path_eval',type=str,   help='path to the groundtruth data for evaluation', required=False)
parser.add_argument('--filenames_file_eval', type=str, help='path to the filenames text file', required=True)
parser.add_argument('--input_height', type=int, help='input height', default=480)
parser.add_argument('--input_width', type=int, help='input width', default=640)
parser.add_argument('--max_depth',                 type=float, help='maximum depth in estimation', default=10)
parser.add_argument('--min_depth_eval',type=float, help='minimum depth for evaluation', default=1e-3)
parser.add_argument('--max_depth_eval', type=float, help='maximum depth in estimation', default=80)
parser.add_argument('--checkpoint_path', type=str, help='path to a specific checkpoint to load', default='')
parser.add_argument('--dataset', type=str, help='dataset to train on', default='nyu')
parser.add_argument('--do_kb_crop', help='if set, crop input images as kitti benchmark images', action='store_true')
parser.add_argument('--save_viz', help='if set, save visulization of the outputs', action='store_true')
parser.add_argument('--gray', help='Use gray images for testing', action='store_true')


if sys.argv.__len__() == 2:
    arg_filename_with_prefix = '@' + sys.argv[1]
    args = parser.parse_args([arg_filename_with_prefix])
else:
    args = parser.parse_args()

if args.dataset == 'kitti' or args.dataset == 'nyu' or args.dataset == '12scenes' or args.dataset == 'iitd':
    from dataloaders.dataloader import NewDataLoader
elif args.dataset == 'kittipred':
    from dataloaders.dataloader_kittipred import NewDataLoader

model_dir = os.path.dirname(args.checkpoint_path)
sys.path.append(model_dir)


def get_num_lines(file_path):
    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()
    return len(lines)


def test(params):
    """Test function."""
    #args.mode = 'test'
    args.distributed = False
    args.mode = 'online_eval'
    dataloader = NewDataLoader(args, args.mode)

    
    model = NewCRFDepth(version='large07', inv_depth=False, max_depth=args.max_depth)
    model = torch.nn.DataParallel(model)
    
    checkpoint = torch.load(args.checkpoint_path)
    model.load_state_dict(checkpoint['model'])
    model.eval()
    model.cuda()

    num_params = sum([np.prod(p.size()) for p in model.parameters()])
    print("Total number of parameters: {}".format(num_params))

    num_test_samples = get_num_lines(args.filenames_file_eval)

    with open(args.filenames_file_eval) as f:
        lines = f.readlines()

    print('now testing {} files with {}'.format(num_test_samples, args.checkpoint_path))

    pred_depths = []
    gt_depths = []
    images = []
    start_time = time.time()
    #save_name = 'models/result_' + args.model_name
    save_name = 'visualisations/result_' + args.dataset + "_" + args.filenames_file_eval.split("/")[-1].split("_")[-1].split(".")[-2] + ("_gray" if args.gray else "")
    os.makedirs(save_name,exist_ok=True)
    
    try:
        
        os.mkdir(save_name + '/raw')
        #os.mkdir(save_name + '/cmap')
        os.mkdir(save_name + '/rgb')
        os.mkdir(save_name + '/gt')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    with torch.no_grad():
        for i, sample in enumerate(tqdm(dataloader.data)):
            image = Variable(sample['image'].cuda())
            has_valid_depth = sample['has_valid_depth']
            if not has_valid_depth:
                # print('Invalid depth. continue.')
                continue
            gt_depth = sample['depth']
            

            # Predict
            depth_est = model(image)
            post_process = True
            if post_process:
                image_flipped = flip_lr(image)
                depth_est_flipped = model(image_flipped)
                depth_est = post_process_depth(depth_est, depth_est_flipped)

            if args.dataset == "kitti":
                pred_depth = (depth_est.cpu().numpy().squeeze() * 256.0 ).astype(np.uint16)
                image = (image.cpu().numpy().squeeze() * 255).astype(np.uint8)
                gt_depth = (gt_depth.numpy().squeeze() * 256.0).astype(np.uint16)

            elif args.dataset == "iitd":
                pred_depth = depth_est.cpu().numpy().squeeze()
                pred_depth[pred_depth < args.min_depth_eval] = args.min_depth_eval
                pred_depth[pred_depth > 6.0] = 6.0
                pred_depth[np.isinf(pred_depth)] = 6.0
                pred_depth[np.isnan(pred_depth)] = args.min_depth_eval

                
                pred_depth = (pred_depth * 1000.0).astype(np.uint16)
                image = (image.cpu().numpy().squeeze() * 255).astype(np.uint8)
                gt_depth = (gt_depth.numpy().squeeze() * 1000.0).astype(np.uint16)
            else:
                print("please change here for you dataset !!")
                sys.exit(0)
            
            #print_minmax(gt_depth,"gt_depth after")
            #print_minmax(pred_depth, "pred_depth")
            
            image = image.transpose(1,2,0)
            image = image[:,:,::-1] #because cv2.imwrite assumes in BGR format.
            #print(image.shape)
            #sys.exit(0)
            if args.do_kb_crop:
                height, width = 352, 1216
                top_margin = int(height - 352)
                left_margin = int((width - 1216) / 2)
                pred_depth_uncropped = np.zeros((height, width), dtype=np.uint16)
                pred_depth_uncropped[top_margin:top_margin + 352, left_margin:left_margin + 1216] = pred_depth
                pred_depth = pred_depth_uncropped                

            #save pred_depth, image and gt_depths
            #print_minmax(gt_depth,"gt_depth")
            cv2.imwrite(save_name + f'/raw/{i:06d}.png',pred_depth)
            cv2.imwrite(save_name + f'/gt/{i:06d}.png',gt_depth)
            cv2.imwrite(save_name + f'/rgb/{i:06d}.png',image)
            # pred_depths.append(pred_depth)
            # gt_depths.append(gt_depth)
            # images.append(image)

    elapsed_time = time.time() - start_time
    print('Elapesed time: %s' % str(elapsed_time))
    print('Done.')

    os.makedirs(save_name+"/orig_rgb/",exist_ok=True)
    i = 0
    print(len(lines),num_test_samples)
    for s in tqdm(range(num_test_samples)):
        if lines[s].split()[1] == "None": 
            print("continue")
            continue
        if args.dataset == 'kitti' or args.dataset == 'iitd':
            orig_rgb_path = os.path.join(args.data_path_eval, lines[s].split()[0])
            orig_rgb = cv2.imread(orig_rgb_path,-1)
            cv2.imwrite(save_name + f'/orig_rgb/{i:06d}.png'  , orig_rgb)
            i+=1
    print()
    print(f"{i} orig_rgb saved!!")



    """
    #save_name = 'models/result_' + args.model_name
    save_name = 'visualisations/result_' + args.dataset + ("_gray" if args.gray else "")
    os.makedirs(save_name,exist_ok=True)
    
    print('Saving result pngs..')
    if not os.path.exists(save_name):
        try:
            os.mkdir(save_name)
            os.mkdir(save_name + '/raw')
            #os.mkdir(save_name + '/cmap')
            os.mkdir(save_name + '/rgb')
            os.mkdir(save_name + '/gt')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    print("len(line) = ",len(lines))
    for i in tqdm(range(len(images))):
    #for s in tqdm(range(num_test_samples)):


        # if lines[s].split()[1] == "None": 
        #     continue
        if args.dataset == 'kitti':
            date_drive = lines[s].split('/')[1]
            filename_pred_png = save_name + '/raw/' + date_drive + '_' + lines[s].split()[0].split('/')[-1].replace(
                '.jpg', '.png')
            filename_cmap_png = save_name + '/cmap/' + date_drive + '_' + lines[s].split()[0].split('/')[
                -1].replace('.jpg', '.png')
            filename_image_png = save_name + '/rgb/' + date_drive + '_' + lines[s].split()[0].split('/')[-1]
            #filename_gtnorm_png = save_name + '/gt_normalized/' + scene_name + '_' + lines[s].split()[0].split('/')[2].replace(
                #'.jpg', '.png')
            filename_gt_png = save_name + '/gt/' + date_drive + '_' + lines[s].split()[0].split('/')[2].replace(
                '.jpg', '_gt.png')

        elif args.dataset == 'kittipred':
            filename_pred_png = save_name + '/raw/' + lines[s].split()[0].split('/')[-1].replace('.jpg', '.png')
            filename_cmap_png = save_name + '/cmap/' + lines[s].split()[0].split('/')[-1].replace('.jpg', '.png')
            filename_image_png = save_name + '/rgb/' + lines[s].split()[0].split('/')[-1]
        else:
            # scene_name = lines[s].split()[0].split('/')[0]
            # filename_pred_png = save_name + '/raw/' + scene_name + '_' + lines[s].split()[0].split('/')[1].replace(
            #     '.jpg', '.png')
            # filename_cmap_png = save_name + '/cmap/' + scene_name + '_' + lines[s].split()[0].split('/rgb_')[1].replace(
            #     '.jpg', '.png')
            # filename_gt_png = save_name + '/gt/' + scene_name + '_' + lines[s].split()[0].split('/rgb_')[1].replace(
            #     '.jpg', '_gt.png')
            # filename_image_png = save_name + '/rgb/' + scene_name + '_' + lines[s].split()[0].split('/rgb_')[1]

            scene_name = lines[s].split()[0].split('/')[0]
            filename_pred_png = save_name + '/raw/' + scene_name + '_' + lines[s].split()[0].split('/')[2].replace(
                '.jpg', '.png')
            filename_gtnorm_png = save_name + '/gt_normalized/' + scene_name + '_' + lines[s].split()[0].split('/')[2].replace(
                '.jpg', '.png')
            filename_gt_png = save_name + '/gt/' + scene_name + '_' + lines[s].split()[0].split('/')[2].replace(
                '.jpg', '_gt.png')
            filename_image_png = save_name + '/rgb/' + scene_name + '_' + lines[s].split()[0].split('/')[2]
        
        #rgb
        rgb_path = os.path.join(args.data_path, './' + lines[s].split()[0])
        image = cv2.imread(rgb_path)

        #gt_depth
        if args.dataset == 'nyu':
            gt_path = os.path.join(args.data_path, './' + lines[s].split()[1])
            gt = cv2.imread(gt_path, -1).astype(np.float32) / 1000.0  # Visualization purpose only
            gt[gt == 0] = np.amax(gt)
        elif args.dataset=="kitti":

            gt_path = os.path.join(args.data_path, lines[s].split()[0].split('/')[0] , lines[s].split()[1])
            print("gt_ptah ", gt_path)
            gt = cv2.imread(gt_path, -1).astype(np.float32) / 1000.0  # Visualization purpose only
            gt[gt == 0] = np.amax(gt)
        
        #pred_depth
        pred_depth = pred_depths[s]
        if args.dataset == 'kitti' or args.dataset == 'kittipred':
            pred_depth_scaled = pred_depth * 256.0
        else:
            pred_depth_scaled = pred_depth * 1000.0
        pred_depth_scaled = pred_depth_scaled.astype(np.uint16)

        #save pred_depth
        cv2.imwrite(filename_pred_png, pred_depth_scaled, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        
        if args.save_viz:

            #save rgb
            cv2.imwrite(filename_image_png, image[10:-1 - 9, 10:-1 - 9, :])
            if args.dataset == 'nyu' or args.dataset=="kitti":

                #save gtnorm
                #plt.imsave(filename_gtnorm_png, (10 - gt) / 10, cmap='plasma')

                #save gt
                plt.imsave(filename_gt_png, gt)
                # pred_depth_cropped = pred_depth[10:-1 - 9, 10:-1 - 9]
                #plt.imsave(filename_cmap_png, (10 - pred_depth) / 10, cmap='plasma')
            #else:
                #plt.imsave(filename_cmap_png, np.log10(pred_depth), cmap='Greys')
    
    return
    """

if __name__ == '__main__':
    test(args)

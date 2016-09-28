#!/usr/bin/env python
"""Gets the CAABB, number of points and average density for a point cloud"""

import argparse, traceback, sys, math, time, os
from pympc import utils

def run(inputFolder, numberProcs, targetSize):
    (_, tcount, tminx, tminy, tminz, tmaxx, tmaxy, tmaxz, _, _, _) = utils.getPCFolderDetails(inputFolder, numberProcs)
    #convert to integers
    tminx = int(math.ceil(tminx))
    tminy = int(math.ceil(tminy))
    tminz = int(math.ceil(tminz))
    tmaxx = int(math.floor(tmaxx))
    tmaxy = int(math.floor(tmaxy))
    tmaxz = int(math.floor(tmaxz))

    tRangeX = tmaxx - tminx
    tRangeY = tmaxy - tminy
    tRangeZ = tmaxz - tminz

    density2  = float(tcount) / (tRangeX*tRangeY)
    #density3  = float(tcount) / (tRangeX*tRangeY*tRangeZ)

    maxRange = max((tRangeX, tRangeY, tRangeZ))

    (minX,minY,minZ,maxX,maxY,maxZ) = (tminx, tminy, tminz, tminx + maxRange, tminy + maxRange, tminz + maxRange)

    print('AABB: ', tminx, tminy, tminz, tmaxx, tmaxy, tmaxz)
    print('#Points:' , tcount)
    print('Average density [pts / m2]:' , density2)
    #print('Average density [pts / m3]:' , density3)

    deepSpacing = 1 / math.sqrt(density2)

    spacing = math.ceil(maxRange / math.sqrt(targetSize))

    numlevels = 0
    lspacing = spacing
    while lspacing > deepSpacing:
        numlevels+=1
        lspacing = lspacing / 2
    numlevels+=1

    print('Suggested Potree-OctTree CAABB: ', minX,minY,minZ,maxX,maxY,maxZ)
    print('Suggested Potree-OctTree spacing: ', spacing)
    print('Suggested Potree-OctTree number of levels: ', numlevels)


def argument_parser():
    """ Define the arguments and return the parser object"""
    parser = argparse.ArgumentParser(
    description="Gets the bounding box of the points in the files of the input folder. Also computes the number of points and the density. It also suggests spacing and number of levels to use for PotreeConverter")
    parser.add_argument('-i','--input',default='',help='Input folder with the point cloud files',type=str, required=True)
    parser.add_argument('-c','--proc',default=1,help='Number of processes [default is 1]',type=int)
    parser.add_argument('-t','--target',default=60000,help='Target average number of points per OctTree node [default is 60000]',type=int)
    return parser

def main():
    args = argument_parser().parse_args()
    print('Input folder: ' , args.input)
    print('Number of processes: ' , args.proc)
    print('Target node size: ' , args.target)

    try:
        t0 = time.time()
        print('Starting ' + os.path.basename(__file__) + '...')
        run(args.input, args.proc, args.target)
        print('Finished in %.2f seconds' % (time.time() - t0))
    except:
        print('Execution failed!')
        print(traceback.format_exc())

if __name__ == "__main__":
    main()

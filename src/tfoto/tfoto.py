import os
import glob
import re
from wand.image import Image
import multiprocessing
from multiprocessing import Process

from .utils import DEBUG
import utils

my_settings = dict()


def process_dirs(dirs, image_settings):
    CWD = os.getcwd()
    DEBUG('Input dirs = %s' % dirs)
    DEBUG('CWD = %s' % CWD)
    global my_settings
    my_settings = image_settings
    file_list = []
    for item in dirs:
        os.chdir(item)
        wd = os.getcwd()
        files = []
        for pattern in image_settings['fmatch']:
            files += glob.glob(pattern)

        for aFile in files:
            file_list += [wd + '/' + aFile]
            os.chdir(CWD)

    # Distribute the big list to all the threads
    thread_no = multiprocessing.cpu_count()
    print "Number of threads = %d" % thread_no
    print "Total files to process = %d" % len(file_list)
    procs = []
    pivot = 0
    part_size = len(file_list)/thread_no
    args_array = []
    for i in range(thread_no):
        args_array.append(file_list[pivot:part_size*(i+1)])
        pivot += part_size

    remain = file_list[pivot:]
    for i in range(len(remain)):
        args_array[i].append(remain[i])

    DEBUG('file_list = %s' % file_list)
    DEBUG('args_array = %s' % args_array)
    for i in range(thread_no):
        procs.append(Process(target=process_image, args=(args_array[i],)))
        procs[i].start()

    # The first spawned threads tend to have more work. So we wait
    # for the last threads first because they tend to finish first.
    for i in range(thread_no):
        DEBUG("joining thread %d" % (thread_no-i-1))
        procs[thread_no-i-1].join()

    os.chdir(CWD)


def process_image(images):
    DEBUG(images)
    global my_settings
    re_obj = re.compile('\.[^\.]+$')
    radius, sigma = [float(s) for s in my_settings['sharpen'].split('x')]
    for item in images:
        output = re.sub(re_obj, '.jpg', item)
        DEBUG('output=%s' % output)
        if utils.DRY_RUN is False:
            with Image(filename=item) as img:
                img.compression_quality = my_settings['quality']
                img.transform(resize=my_settings['scale'])
                img.unsharp_mask(radius=radius, sigma=sigma, amount=85,
                                 threshold=4)
                if 'strip' == my_settings['profile']:
                    img.strip()
                img.save(filename=output)

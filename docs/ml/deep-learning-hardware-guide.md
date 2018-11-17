# Deep Learning Hardware Guide

http://timdettmers.com/2015/03/09/deep-learning-hardware-guide/

## Conclusion / TL;DR

GPU: GTX 680 or GTX 960 (no money); GTX 980 (best performance); GTX Titan (if you need memory); GTX 970 (no convolutional nets)

CPU: Two threads per GPU; full 40 PCIe lanes and correct PCIe spec (same as your motherboard); > 2GHz; cache does not matter;

RAM: Use asynchronous mini-batch allocation; clock rate and timings do not matter; buy at least as much CPU RAM as you have GPU RAM;

Hard drive/SSD: Use asynchronous batch-file reads and compress your data if you have image or sound data; a hard drive will be fine unless you work with 32 bit floating point data sets with large input dimensions

PSU: Add up watts of GPUs + CPU + (100-300) for required power; get high efficiency rating if you use large conv nets; make sure it has enough PCIe connectors (6+8pins) and watts for your (future) GPUs

Cooling: Set coolbits flag in your config if you run a single GPU; otherwise flashing BIOS for increased fan speeds is easiest and cheapest; use water cooling for multiple GPUs and/or when you need to keep down the noise (you work with other people in the same room)

Motherboard: Get PCIe 3.0 and as many slots as you need for your (future) GPUs (one GPU takes two slots; max 4 GPUs per system)

Monitors: If you want to upgrade your system to be more productive, it might make more sense to buy an additional monitor rather than upgrading your GPU

## CPU
What does the CPU do for deep learning? The CPU does little computation when you run your deep nets on a GPU, but your CPU does still work on these things:

* Writing and reading variables in your code
* Executing instructions such as function calls
* Initiating function calls on your GPU
* Creating mini-batches from data
* Initiating transfers to the GPU


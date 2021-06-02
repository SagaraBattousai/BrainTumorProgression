
Brain Tumor Progression Dataset
===============================

Files
=====
:Directories:
  Directories 01 - 11 include pairs of Pre and Post T1 MRI Scans and Masks
  (four per directory)

:supplementary.csv:
  CSV file that gives additional information for the data and includes details
  of what slices were removed in order to transform the original data into this
  dataset. This file is used by ``process.py`` (explained below) to modify the
  original dataset into this dataset.

:process.py:
  Python script to modify original dataset into this dataset, contains
  useful helper functions to use in the interpreter or script to make further
  modifications. This file is messy and unneeded but gives a technical 
  description of the changes made to supplement the explanation below.

:metadata.csv:
  The metadata file from the TCIA downloader showing the raw data this dataset
  is based on/downloaded from.

:licence.html:
  The licence file from the TCIA downloader. This is the original licence file
  that is included when the data is downloaded from the source.

:README.rst:
  This document

Data References and Usage
=========================

This repository includes data from the Brain-Tumor-Progression collection
published by `The Cancer Imaging Archive`. The original data has been modified
in the following ways: Firstly all DICM image slices per set have been combined
into one Gzipped NIfTI file, renaming the resulting NIfTI images 
Pre.... and Post... for the first and second scan respectivly, for both the
MRI Scans and associated tumor masks resulting in four .nii.gz images.
The images have all been resized to 256 X 256 using Nearest Neighbors
interpolation and the number of slices was first reduces to 22, for some sets
that required a few slides to be dropped and resulted in a closer relationship
between Pre and Post slices for the same slice number, for others no change was
required. Following that the slices were then padded with blank slides to bring
the final count to 24 slices each; this was done so that three subsample
convolutional layers could be composed without ending up with decimal dimensions
(24 % 2^3 = 0). 

Users of this data must abide by the TCIA Data Usage Policy and the `Creative Commons Attribution 3.0 Unported License`_ under which it has been published. Any publications discussing these data should include references to the following:

  Data Citation
    Schmainda KM, Prah M (2018). Data from Brain-Tumor-Progression. The Cancer Imaging Archive. http://doi.org/10.7937/K9/TCIA.2018.15quzvnb

    Kathleen M Schmainda, Melissa A Prah, Jennifer M Connelly, Scott D Rand. (2016). Glioma DSC-MRI Perfusion Data with Standard Imaging and ROIs [ Dataset ] . The Cancer Imaging Archive. DOI: 10.7937/K9/TCIA.2016.5DI84Js8

  Publication Citation
    Schmainda KM, Prah MA, Rand SD, Liu Y, Logan B, Muzi M, Rane SD, Da X, Yen YF, Kalpathy-Cramer J, Chenevert TL, Hoff B, Ross B, Cao Y, Aryal MP, Erickson B, Korfiatis P, Dondlinger T, Bell L, Hu L, Kinahan PE, Quarles CC. (2018). Multisite Concordance of DSC-MRI Analysis for Brain Tumors: Results of a National Cancer Institute Quantitative Imaging Network Collaborative Project. American Journal of Neuroradiology, 39(6), 1008–1016. DOI: 10.3174/ajnr.a5675


  TCIA Citation
    Clark K, Vendt B, Smith K, Freymann J, Kirby J, Koppel P, Moore S, Phillips S, Maffitt D, Pringle M, Tarbox L, Prior F. The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository, Journal of Digital Imaging, Volume 26, Number 6, December, 2013, pp 1045-1057. https://doi.org/10.1007/s10278-013-9622-7


.. _`The Cancer Imaging Archive`: https://cancerimagingarchive.net
.. _`Creative Commons Attribution 3.0 Unported License`: https://creativecommons.org/licenses/by/3.0/

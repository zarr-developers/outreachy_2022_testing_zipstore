import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf
import zarr
import numpy as np
from osgeo import gdal

def main():
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
    assert train_images.shape == (60000, 28, 28)
    assert train_labels.shape == (60000,)

    assert test_images.shape == (10000, 28, 28)
    assert test_labels.shape == (10000,)

    # write to zipstore
    store = zarr.ZipStore("data.zip", mode="w")
    z = zarr.zeros(train_images.shape, store=store)
    z[:] = train_images
    store.close()

    # create a dataset using the zarr driver
    z_ds = gdal.GetDriverByName("ZARR").Create("/path/to/valid/dir/z_ds", train_images.shape[1], train_images.shape[2], 1, gdal.GDT_Int32)
    z_ds = None

if __name__ == "__main__":
    main()

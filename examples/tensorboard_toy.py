# TRAINS - Example of tensorboard with tensorflow (without any actual training)
#
import tensorflow as tf
import numpy as np
import cv2
from time import sleep
#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()

from trains import Task
task = Task.init(project_name='examples', task_name='tensorboard toy example')


k = tf.placeholder(tf.float32)

# Make a normal distribution, with a shifting mean
mean_moving_normal = tf.random_normal(shape=[1000], mean=(5*k), stddev=1)
# Record that distribution into a histogram summary
tf.summary.histogram("normal/moving_mean", mean_moving_normal)
tf.summary.scalar("normal/value", mean_moving_normal[-1])

# Make a normal distribution with shrinking variance
variance_shrinking_normal = tf.random_normal(shape=[1000], mean=0, stddev=1-(k))
# Record that distribution too
tf.summary.histogram("normal/shrinking_variance", variance_shrinking_normal)
tf.summary.scalar("normal/variance_shrinking_normal", variance_shrinking_normal[-1])

# Let's combine both of those distributions into one dataset
normal_combined = tf.concat([mean_moving_normal, variance_shrinking_normal], 0)
# We add another histogram summary to record the combined distribution
tf.summary.histogram("normal/bimodal", normal_combined)
tf.summary.scalar("normal/normal_combined", normal_combined[0])

# Add a gamma distribution
gamma = tf.random_gamma(shape=[1000], alpha=k)
tf.summary.histogram("gamma", gamma)

# And a poisson distribution
poisson = tf.random_poisson(shape=[1000], lam=k)
tf.summary.histogram("poisson", poisson)

# And a uniform distribution
uniform = tf.random_uniform(shape=[1000], maxval=k*10)
tf.summary.histogram("uniform", uniform)

# Finally, combine everything together!
all_distributions = [mean_moving_normal, variance_shrinking_normal, gamma, poisson, uniform]
all_combined = tf.concat(all_distributions, 0)
tf.summary.histogram("all_combined", all_combined)

# convert to 4d [batch, col, row, RGB-channels]
image = cv2.imread('./samples/picasso.jpg')
image = image[:, :, 0][np.newaxis, :, :, np.newaxis]
# image = image[np.newaxis, :, :, :]  # test greyscale image

# un-comment to add image reporting
tf.summary.image("test", image, max_outputs=10)

# Setup a session and summary writer
summaries = tf.summary.merge_all()
sess = tf.Session()

logger = task.get_logger()

# Use original FileWriter for comparison , run:
# % tensorboard --logdir=/tmp/histogram_example
writer = tf.summary.FileWriter("/tmp/histogram_example")

# Setup a loop and write the summaries to disk
N = 40
for step in range(N):
    k_val = step/float(N)
    summ = sess.run(summaries, feed_dict={k: k_val})
    writer.add_summary(summ, global_step=step)

print('Done!')

# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from pymc import Poisson
from pymc import Uniform
from pymc.distributions import poisson_like

from babtest.models.abstract_model import AbstractModel


class PoissonModel(AbstractModel):

    def __init__(self, control, variant):
        """Init.

        :param np.array control: 1 dimensional array of observations for control group
        :param np.array variant: 1 dimensional array of observations for variant group

        """
        AbstractModel.__init__(self, control, variant)
        self.params = ['mu']

    def set_models(self):
        """Define models for each group.

        :return: None
        """
        for group in ['control', 'variant']:
            self.stochastics[group] = Poisson(
                group,
                self.stochastics[group + '_mu'],
                value=getattr(self, group),
                observed=True)

    def set_priors(self):
        """set parameters prior distributions.

        Hardcoded behavior for now, with non committing prior knowledge.

        :return: None
        """
        obs = np.concatenate((self.control, self.variant))
        obs_mean = np.mean(obs)
        for group in ['control', 'variant']:
            self.stochastics[group + '_mu'] = Uniform(group + '_mu', 0, 100 * obs_mean)

    def draw_distribution(self, group, x, i):
        """Draw the ith sample distribution from the model, and compute its values for each element of x.

        :param string group: specify group, control or variant
        :param numpy.array x: linspace vector, for which to compute probabilities
        :param int i: index of the distribution to compute

        :return: values of the model for the ith distribution
        :rtype: numpy.array
        """
        mu = self.stochastics[group + '_mu'].trace()[i]
        return np.exp([poisson_like(xi, mu) for xi in x])

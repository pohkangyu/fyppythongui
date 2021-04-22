from statsmodels.tsa.stattools import adfuller
import statsmodels.tsa.vector_ar.vecm as vecm

allowedPercentage = {"1%" : 0.01, "5%" : 0.05, "10%" : 0.10}

class StationaryTestModule():

    def runAugmentedDickeyFuller(self, time_series, name, adfsignificant):
        result = adfuller(time_series.values)
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        print('Critical Values:')

        for key, value in result[4].items():
            print('\t%s: %.3f' % (key, value))
        rejected = []
        if result[0] > result[4][adfsignificant]:
            rejected += [name]
        return rejected

    def runCointegrationJohansen(self, johansenSignificant):
        vec_rank = vecm.select_coint_rank(self.data, det_order = 0 , k_ar_diff = 1, method = 'trace', signif=johansenSignificant)
        num_tests = min(vec_rank.rank, vec_rank.neqs-1)
        data = [[i, vec_rank.r_1[i], vec_rank.test_stats[i], vec_rank.crit_vals[i]] for i in range(num_tests + 1)]
        if (len(data) == data[0][1]):
            return True
        else:
            return False

    def getResult(self, data, adfsignificant, johansenSignificant):
        self.data = data
        self.rejected = []

        if not (adfsignificant in list(allowedPercentage.keys())):
            raise ValueError("ADF signifcant error")

        if not (johansenSignificant in list(allowedPercentage.keys())):
            raise ValueError("ADF signifcant error")

        johansenSignificant = allowedPercentage[johansenSignificant]

        for column in self.data:
            self.rejected += self.runAugmentedDickeyFuller(self.data[column], column, adfsignificant)
        if len(self.rejected) == 0:
            text = "Pass on the basis that all columns are stationary"
            print(text)
            return True, text
        elif (self.runCointegrationJohansen(johansenSignificant)):
            text = "Pass on the basis that system are co-integrated, columns that are not stationary includes: " + str(self.rejected)
            print(text)
            return True, text
        else:
            text = "Fail, system is not co-integrated and columns: " + str(self.rejected) + " are not stationary"
            print(text)
            return False, text

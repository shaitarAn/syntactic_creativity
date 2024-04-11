import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from scipy.stats import t
from numpy import mean
from numpy import std
from numpy import sqrt
from numpy import var

# Path to your CSV file
csv_file = "../results/par3_xwr.csv"
print(csv_file)

# group by the column "book" and plot columns GT,human1,human2,human3 if human3 is present
df = pd.read_csv(csv_file)

# df_grouped = df.groupby("book")

# # for each book create a boxplot of the columns GT,human1,human2 and human3 if present
# for name, group in df_grouped:
#     print(name)
#     print(group)
#     # print column "lang" of the group
#     print(group["source_lang"])
#     group.boxplot(column=["GT", "human1", "human2", "human3"])
#     plt.title(name)
#     plt.show()

df_lang = df.groupby("source_lang")
# start a dataframe to store the results
results = pd.DataFrame(columns=["source_lang", "d1", "d2", "d3", "p_value1", "p_value2", "p_value3", "t_statistic1", "t_statistic2", "t_statistic3"])

def analyze_cohend(d):
    if 0 < d < 0.2:
        return 'negligible +'
    elif 0.2 <= d < 0.5:
        return 'small +'
    elif 0.5 <= d < 0.8:
        return 'medium +'
    elif d >= 0.8:
        return 'large +'
    elif 0 > d > -0.2:
        return 'negligible -'
    elif -0.2 >= d > -0.5:
        return 'small -'
    elif -0.5 >= d > -0.8:
        return 'medium -'
    elif d <= -0.8:
        return 'large -'
    
def calculate_confidence_interval(n1, n2, d):
    # Calculate standard error of Cohen's d
    SE_d = sqrt(1/n1 + 1/n2)

    # Calculate degrees of freedom
    df = n1 + n2 - 2

    # Set confidence level
    confidence_level = 0.95
    alpha = 1 - confidence_level

    # Calculate critical t-value for one-tailed test
    t_critical = t.ppf(1-alpha, df)

    # Calculate confidence interval for Cohen's d
    CI_d = (d - t_critical * SE_d, d + t_critical * SE_d)

    return CI_d 


for name, group in df_lang:
    print(group)
    # calculate the effect size
    data1 = group["GT"]
    data2 = group["human1"]
    data3 = group["human2"]
    # calculate the size of the two samples
    n1, n2, n3 = len(data1), len(data2), len(data3)
    # calculate the variance of the two samples
    var1, var2, var3 = var(data1, ddof=1), var(data2, ddof=1), var(data3, ddof=1)
    # calculate the pooled standard deviation
    s1 = sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    s2 = sqrt(((n1 - 1) * var1 + (n3 - 1) * var3) / (n1 + n3 - 2))
    # calculate the means of the two samples
    u1, u2, u3 = mean(data1), mean(data2), mean(data3)
    
    # calculate the effect size
    d1 = (u1 - u2) / s1
    d2 = (u1 - u3) / s2
    
    print(name)

    # ########## GT vs human1 ##########
    print("*"*20)
    print("GT vs human1:")
    lower1, upper1 = calculate_confidence_interval(n1, n2, d1)
    # present results in this format: effect of .47 with the 95% CI [.32, .62]
    print("Effect of", round(d1, 2), "with the 95% CI [", round(lower1, 2), ",", round(upper1, 2), "]")
    # interpret the effect size
    print(analyze_cohend(d1))
    # calculate the t statistic
    t_statistic1, p_value1 = ttest_ind(data1, data2)
    print('t=%.3f, p=%.3f' % (t_statistic1, p_value1))
    # interpret the result
    alpha = 0.05
    if p_value1 > alpha:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')

    # ########## GT vs human2 ##########
    print("*"*20)
    print("GT vs human2:")
    lower2, upper2 = calculate_confidence_interval(n1, n3, d2)
    # return rounder values
    print("Effect of", round(d2, 2), "with the 95% CI [",round(lower2, 2), ",", round(upper2, 2), "]")
    # interpret the effect size
    print(analyze_cohend(d2))

    t_statistic2, p_value2 = ttest_ind(data1, data3)
    print('t=%.3f, p=%.3f' % (t_statistic2, p_value2))
    # interpret the result
    if p_value2 > alpha:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')
    
    # ########## plot the results ##########
    group.boxplot(column=["GT", "human1", "human2", "human3"])
    plt.title(name)
    # plt.show()

    # if human3 is present calculate the effect size and the t statistic
    if "human3" in group.columns:
        data4 = group["human3"]
        n4 = len(data4)
        var4 = var(data4, ddof=1)
        s3 = sqrt(((n1 - 1) * var1 + (n4 - 1) * var4) / (n1 + n4 - 2))
        u4 = mean(data4)
        d3 = (u1 - u4) / s3
        lower3, upper3 = calculate_confidence_interval(n1, n4, d3)
        print("GT vs human3:")
        print("Effect of", round(d3, 2), "with the 95% CI [", round(lower3, 2), ",", round(upper3, 2), "]")
        print(analyze_cohend(d3))
        t_statistic3, p_value3 = ttest_ind(data1, data4)
        print('t=%.3f, p=%.3f' % (t_statistic3, p_value3))
        if p_value3 > alpha:
            print('Same distributions (fail to reject H0)')
        else:
            print('Different distributions (reject H0)')

    # store the results in the dataframe
    results = results.append({"source_lang": name, "d1": d1, "d2": d2, "d3": d3, "p_value1": p_value1, "p_value2": p_value2, "p_value3": p_value3, "t_statistic1": t_statistic1, "t_statistic2": t_statistic2, "t_statistic3": t_statistic3}, ignore_index=True)

print(results)
# save the results to a CSV file
results.to_csv("../results/par3_d_results.csv", index=False)

# make a plot of the results
# convert negative values to positive for d1, d2 and d3
results["d1"] = results["d1"].abs()
results["d2"] = results["d2"].abs()
results["d3"] = results["d3"].abs()

# plot the results
plt.figure(figsize=(10, 6))
plt.title("Effect sizes of GT vs human translators")

# Define the width of each bar
bar_width = 0.25

# Create separate x positions for each group of bars
x1 = results.index - bar_width
x2 = results.index
x3 = results.index + bar_width

# Plot each group of bars
plt.bar(x1, results["d1"], width=bar_width, color='b', label="human1")
plt.bar(x2, results["d2"], width=bar_width, color='g', label="human2")
plt.bar(x3, results["d3"], width=bar_width, color='r', label="human3")

# add legend
plt.legend()

# mark 0.2, 0.5 and 0.8 as the thresholds for small, medium and large effect sizes on the y-axis
plt.axhline(y=0.2, color='r', linestyle='--', label="small")
plt.axhline(y=0.5, color='r', linestyle='--', label="medium")
plt.axhline(y=0.8, color='r', linestyle='--', label="large")

# rotate the x-axis labels
plt.xticks(rotation=45)

plt.show()



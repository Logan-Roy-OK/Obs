import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

def running_mean(var,window):
    return np.convolve(var, np.ones(window)/window, mode='valid')

def norm_std(var):

    var_mean = np.mean(var)
    var_std = np.std(var)
    normed_var = (var-var_mean)/var_std

    return normed_var

def norm_minmax(var):

    var_max = np.max(var)
    var_min = np.min(var)

    normed_var = (var-var_max)/(var_max-var_min)

    return normed_var

def id_diagnostic(var):
    if ((var=='CO2') | (var=='H2O')):
        diag = 'diag_irga'
    elif (var[1:]=='spas'):
        return
    else:
        diag="diag_sonic_"+var[-1:]

    return diag

def plot2things(df,var1,var2,time_min,time_max):
    
    # identify proper diagnostic for given variable
    var_diag1 = id_diagnostic(var1)
    var_diag2 = id_diagnostic(var2)

    # clean data set to only include data within the time serries while also excluding any datapoints with diagnostic flag not 0
    timesrs1 = df['time(hr)'][(df['time(hr)']>time_min)&(df['time(hr)']<time_max)&(df[var_diag1]==0)]
    timesrs2 = df['time(hr)'][(df['time(hr)']>time_min)&(df['time(hr)']<time_max)&(df[var_diag2]==0)]
    varsrs1 = df[var1][(df['time(hr)']>time_min)&(df['time(hr)']<time_max)&(df[var_diag1]==0)]
    varsrs2 = df[var2][(df['time(hr)']>time_min)&(df['time(hr)']<time_max)&(df[var_diag2]==0)]

    # calculate covariance between the two variables
    #covariance = np.cov(norm_std(varsrs1.values),norm_std(varsrs2.values))
    covariance = np.cov(norm_std(varsrs1.values),norm_std(varsrs2.values))

    print("covariance = "+str(covariance[0,1]))

    fig,axs = plt.subplots(2,1)

    axs[0].plot(timesrs1,varsrs1)
    axs[0].set_title(var1)
    axs[0].set_xlabel('time (hr)')
    axs[0].set_ylabel("")

    axs[1].plot(timesrs2,varsrs2)  
    axs[1].set_title(var2)
    axs[1].set_xlabel('time (hr)')
    plt.tight_layout()
    plt.show()


    return

def plot1var(df,var,time_min=0,time_max=23.99):

    # identify proper diagnostic for given variable
    var_diag = id_diagnostic(var)

    # get data within the time interval excluding any data where the diagnostic flag is not 0
    timesrs = df['time(hr)'][(df['time(hr)']>time_min)&(df['time(hr)']<time_max)&(df[var_diag]==0)]
    varsrs = df[var][(df['time(hr)']>time_min)&(df['time(hr)']<time_max)&(df[var_diag]==0)]

    # Calculate variance of the cleaned data
    variance = np.var((varsrs.values))
    print("variance = "+str(variance))

    run_mean = running_mean(varsrs.values,600)

    fig,axs = plt.subplots()

    axs.plot(timesrs,varsrs)
    axs.plot
    axs.set_title(var)
    axs.set_xlabel('time (hr)')
    axs.set_ylabel("")

    plt.tight_layout()
    plt.show()

   
    
    return

def tke_stuff(df,time_min=0,time_max=23.99):
    # limit analysis to data within a desired period
    df_trim = df[(df['time(hr)']>time_min)&(df['time(hr)']<time_max)]

    uprime = df_trim['u1']-df_trim['u1'].mean()
    uprime2 = uprime*uprime
    vprime = df_trim['v1']-df_trim['v1'].mean()
    vprime2 = vprime*vprime
    wprime = df_trim['w1']-df_trim['w1'].mean()
    wprime2 = wprime*wprime

    tke = 0.5*(uprime2+vprime2+wprime2)
    df_trim['tke']=tke
    plt.plot(df_trim['time(hr)'],df_trim['tke'])
    plt.show()
    delt = df['time(hr)'][1]-df['time(hr)'][0]

    y = df_trim['tke']
    x = df_trim['time(hr)']

    N = len(y)
    yf = sp.fft.fft(y.values)
    xf = sp.fft.fftfreq(N,delt)[:N//2]
    plt.loglog(xf, 2.0/N * np.abs(yf[:N//2]))
    #plt.plot(y[0:N//2])
    #plt.xlim((1,600))
    #plt.ylim((0.01,100))
    plt.show()
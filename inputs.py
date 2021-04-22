globalInput = {
    'UploadRow' : {
        'Buttons' :
            {
                'Button1' : {
                    'Text' : 'Select File',
                    'Information' : 'Select and upload a File'
                },
                'Button2' : {
                    'Text' : 'Select Settings',
                    'Information' : 'Select and upload a setting'
                }
            }
    },


    'StationaryCheck' : {
        'InputsChoice' :
            {
                'Input1' : {
                    'Text' : 'ADF Significant',
                    'Choice' : ['1%', '5%', '10%'],
                    'Information' : 'ADF Significant Level'
                },
                'Input2' : {
                    'Text' : 'Johansen Significant',
                    'Choice' : ['1%', '5%', '10%'],
                    'Information' : 'Johansen Significant Level'
                }
            },
        'Buttons' :
            {
                'Button1' : {
                    'Text' : 'Run',
                }
            }
    },

    'MultivariateTE' : {
        'Buttons' :
        {
            'Button1' : {
                'Text' : 'Run',
                'Information' : 'Run the MUTE'
            }
        },
        'InputsChoice' :
            {
                'Input1' : {
                    'Text' : 'cmi_estimator',
                    'Choice' : ['JidtKraskovCMI', 'JidtDiscreteCMI', 'JidtGaussianCMI'],
                    'Information' : 'Estimator to be used for CMI calculation'
                },
            },
        'InputsInteger' :
            {
                'Input1' : {
                    'Text' : 'max_lag_sources',
                    'Information' : "Maximum temporal search depth for candidates in the sources' past in samples",
                    'Default' : '5'
                },
                'Input2' : {
                    'Text' : 'min_lag_sources',
                    'Information' : "Mnimum temporal search depth for candidates in the sources' past in samples",
                    'Default' : '1'
                },

                'Input3' : {
                    'Text' : 'max_lag_target ',
                    'Information' : "Maximum temporal search depth for candidates in the target's past in sample, default=same as max_lag_sources",
                    'Default' : ''
                },
                'Input4' : {
                    'Text' : 'tau_sources',
                    'Information' : "Spacing between candidates in the sources' past in samples, default = 1",
                    'Default' : ''
                },
                'Input5' : {
                    'Text' : 'tau_target',
                    'Information' : "Spacing between candidates in the target's past in sample, default = 1",
                    'Default' : ''
                },
                'Input6' : {
                    'Text' : 'n_perm_max_stat',
                    'Information' : "Number of permutations for Max Stat",
                    'Default' : ''
                },
                'Input7' : {
                    'Text' : 'n_perm_min_stat',
                    'Information' : "Number of permutations for Min Stat",
                    'Default' : ''
                },
                'Input8' : {
                    'Text' : 'n_perm_omnibus',
                    'Information' : "Number of permutations for Omnibus",
                    'Default' : ''
                },
                'Input9' : {
                    'Text' : 'n_perm_max_seq',
                    'Information' : "Number of permutations for Max Sequence",
                    'Default' : ''
                }
            },
        'InputsFloat' :
            {
                'Input1' : {
                    'Text' : 'alpha_max_stats',
                    'Information' : 'Critical alpha level for statistical significance',
                    'Default' : ''
                },
                'Input2' : {
                    'Text' : 'alpha_min_stats',
                    'Information' : 'Critical alpha level for statistical significance',
                    'Default' : ''
                },
                'Input3' : {
                    'Text' : 'alpha_omnibus',
                    'Information' : 'Critical alpha level for statistical significance',
                    'Default' : ''
                }
            },
    },

}

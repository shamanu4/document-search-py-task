def progressbar(
    iteration: int,
    total: int,
    prefix: str = '',
    suffix: str = '',
    decimals: int = 1,
    length: int = 100,
    fill: str = '█'
):
    """
    Call in a loop to create terminal progress bar.

    @params:
        iteration   - Required  : current iteration
        total       - Required  : total iterations
        prefix      - Optional  : prefix string
        suffix      - Optional  : suffix string
        decimals    - Optional  : positive number of decimals in percent complete
        length      - Optional  : character length of bar
        fill        - Optional  : bar fill character
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r', flush=True)
    # Print New Line on Complete
    if iteration == total:
        print()

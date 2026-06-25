class lp:

    def time_to_sal():

        time = []

        start = 8.00
        up = 20.00

        time.append(start)
        time.append(up)

        saln = 1250
        salplus = 1563

        alltime = time[1]-time[0]

        if alltime >8 :
            sal = (alltime - 8)*salplus + 8 * saln
        else:
            sal = alltime * saln

        if time[0] < 5.00 :
            sal += (5.00 - time[0])*300

        if time[1] > 22.00:
            sal += (time[1] - 22.00)*300 

        print(sal)
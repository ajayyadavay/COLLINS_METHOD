from numpy import *
import matplotlib.pyplot as plotting

f = open("INPUT.txt", "r")
data = f.readlines()
f.close()
f_out = open("OUTPUT.txt", "w")

catchment_area = float(data[1])
duration_of_rain_DRH = float(data[3])
all_rain = data[5].split(',')
all_DRH = data[7].split(',')
number_of_iteration = int(data[9])

number_of_rain = len(all_rain)
number_of_DRH = len(all_DRH)
print("Number of rainfall =", number_of_rain)
print("Number of DRH =", number_of_DRH)

rain = [0.0 for i in range(number_of_rain)]
DRH = [0.0 for j in range(number_of_DRH)]

total_rain = 0.0
for i in range(0, number_of_rain, 1):
    # rain[i] = float(data[1].split(',')[i])
    rain[i] = float(all_rain[i])
    total_rain = total_rain + rain[i]

max_rain = max(rain)
print("Maximum rainfall_in_mm = ", max_rain)
print("Total rain = ", total_rain)

Total_DRH = 0.0
for i in range(0, number_of_DRH, 1):
    DRH[i] = float(all_DRH[i])
    Total_DRH = Total_DRH + DRH[i]

print("Non_Zero_DRH_in_m3/s")
print(DRH)

number_of_UH = number_of_DRH - number_of_rain + 1
print("Number of ordinates of UH =", number_of_UH)
Assumed_UH = [0.0 for i in range(number_of_DRH)]

Total_Assumed_UH = 0.0
for i in range(0, number_of_DRH, 1):
    Assumed_UH[i] = round(DRH[i]/total_rain, 1)
    Total_Assumed_UH = Total_Assumed_UH + Assumed_UH[i]

y_previous_corrected_UH = [0.0 for i in range(number_of_DRH+2)]
y_now_corrected_UH = [0.0 for i in range(number_of_DRH+2)]
x_time = [duration_of_rain_DRH * i for i in range(number_of_DRH+2)]
print("x_time_in_hour")
print(x_time)

for iteration in range(number_of_iteration):

    print("------------------------------>>>>>>>>>>>>>>>>> Iteration = ", iteration + 1)

    print("Assumed_UH_in_m3/s/mm")
    print(Assumed_UH)

    Corrected_UH = [0.0 for i in range(number_of_DRH)]

    Total_Corrected_UH = 0.0
    Summation_U = round(catchment_area * 1000 / (duration_of_rain_DRH * 60 * 60), 1)
    for i in range(0, number_of_DRH, 1):
        Corrected_UH[i] = round(Assumed_UH[i] * Summation_U / Total_Assumed_UH, 1)
        Total_Corrected_UH = Total_Corrected_UH + Corrected_UH[i]

    print("Corrected_UH_in_m3/s/mm")
    print(Corrected_UH)

    if iteration == 0:
        for i in range(1, number_of_DRH, 1):
            y_previous_corrected_UH[i] = Corrected_UH[i]
    else:
        for i in range(1, number_of_DRH, 1):
            y_now_corrected_UH[i] = Corrected_UH[i]

    Response = [[0.0 for j in range(number_of_DRH)] for i in range(number_of_rain)]
    k = 0
    max_rain_index = 0
    for i in range(0, number_of_rain, 1):
        for j in range(0, number_of_DRH - k, 1):
            if rain[i] == max_rain:
                max_rain_index = i
                continue
            Response[i][j + k] = round(Corrected_UH[j] * rain[i], 1)
        k = k + 1

    print("Max rain in mm = ", max_rain)
    for i in range(0, number_of_rain, 1):
        if rain[i] == max_rain:
            continue
        print("Response due to rain of ", rain[i], " mm")
        print(Response[i])

    Added_Response = [[0.0 for j in range(number_of_DRH)] for i in range(number_of_rain)]

    for j in range(0, number_of_DRH, 1):
        for i in range(0, number_of_rain, 1):
            if rain[i] == max_rain:
                continue
            Added_Response[0][j] = round(Added_Response[0][j] + Response[i][j], 1)

    print("Added_Response_in_m3/s")
    print(Added_Response[0])

    Max_rain_response = [0.0 for i in range(number_of_DRH)]
    for i in range(0, number_of_DRH-max_rain_index, 1):
        Max_rain_response[i + max_rain_index] = round(DRH[i] - Added_Response[0][i], 1)
        if Max_rain_response[i+max_rain_index] < 0:
            Max_rain_response[i+max_rain_index] = 0

    print("Response_due_to_max_rain_of ", rain[max_rain_index], " mm")
    print(Max_rain_response)

    New_UH = [0.0 for i in range(number_of_DRH)]
    for i in range(0, number_of_DRH, 1):
        New_UH[i] = round(Max_rain_response[i] / rain[max_rain_index], 2)

    print("New UH_in_m3/s/mm")
    print(New_UH)

    Weighted_average = [0.0 for i in range(number_of_DRH)]
    for i in range(0, number_of_DRH, 1):
        Weighted_average[i] = round((Corrected_UH[i] * (total_rain - max_rain) + New_UH[i] * max_rain)/total_rain, 1)

    print("Weighted Average_in_m3/s/mm")
    print(Weighted_average)

    print("Weighted_average of this iteration becomes Assumed_UH of the next iteration")

    f_out.write("------------->>>>>>>>>>>>>>>>>>> ITERATION = ")
    f_out.write(str(iteration + 1))
    f_out.write("\n")
    f_out.write("time\tDRH\tAssumed_UH\tCorrected_UH\t")
    for j in range(number_of_rain):
        f_out.write("Response_for ")
        f_out.write(str(rain[j]))
        f_out.write("\t")

    f_out.write("Add_Response_except_max\t\t")
    f_out.write("New_UH\t\t")
    f_out.write("Weighted_average\n")

    for i in range(0,number_of_DRH,1):
        f_out.write(str(x_time[i+1]))
        f_out.write("\t")
        f_out.write(str(DRH[i]))
        f_out.write("\t")
        f_out.write(str(Assumed_UH[i]))
        f_out.write("\t\t")
        f_out.write(str(Corrected_UH[i]))
        f_out.write("\t\t\t")
        for j in range(number_of_rain):
            if rain[j] == max_rain:
                f_out.write(str(Max_rain_response[i]))
                f_out.write("\t\t\t")
            else:
                f_out.write(str(Response[j][i]))
                f_out.write("\t\t\t")
        f_out.write(str(Added_Response[0][i]))
        f_out.write("\t\t\t")
        f_out.write(str(New_UH[i]))
        f_out.write("\t\t\t")
        f_out.write(str(Weighted_average[i]))
        f_out.write("\n")

    for i in range(0, number_of_DRH, 1):
        Assumed_UH[i] = Weighted_average[i]

    if iteration > 0:
        plotting.plot(x_time, y_previous_corrected_UH)
        plotting.plot(x_time, y_now_corrected_UH)
        plotting.title("UH_PLOT " + str(iteration + 1))
        plotting.xlabel("time (t), hr")
        plotting.legend(['Previous', 'New'])
        plotting.ylabel("UH_ordinate, m3/s/mm")
        plotting.savefig("UH_" + str(iteration + 1) + ".png", bbox_inches="tight")
        plotting.show()
        for i in range(1, number_of_DRH, 1):
            y_previous_corrected_UH[i] = y_now_corrected_UH[i]

f_out.close()
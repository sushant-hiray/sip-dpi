from data import *


########################## For calculating average values of various times #################
avg_first_request_bono = 0
avg_first_request_sprout = 0
avg_first_request_hs = 0
avg_first_response_sprout = 0
avg_first_response_bono = 0
avg_second_request_bono = 0
avg_second_request_sprout = 0
avg_second_request_hs = 0
avg_second_response_sprout = 0
avg_second_response_bono = 0



def calculate_time_diff():
    global avg_first_request_bono 
    global avg_first_request_sprout
    global avg_first_request_hs
    global avg_first_response_sprout
    global avg_first_response_bono
    global avg_second_request_bono
    global avg_second_request_sprout
    global avg_second_request_hs
    global avg_second_response_sprout
    global avg_second_response_bono
    size = len(left_bono_second_response)
    file_data = open("graph_arrays","a")
    for key in left_bono_second_response:
      if came_bono_first_request.has_key(key) != False:
        if left_bono_first_request.has_key(key) != False:
          avg_first_request_bono += left_bono_first_request[key] - came_bono_first_request[key]
      if came_sprout_first_request.has_key(key) != False:
        if left_sprout_first_request.has_key(key) != False:
          if left_sprout_first_request[key] < came_sprout_first_request[key]:
            print "First Request - " + key + " " + str(left_sprout_first_request[key]) + " " + str(came_sprout_first_request[key])
          else:
            avg_first_request_sprout += left_sprout_first_request[key] - came_sprout_first_request[key]
      if came_hs_first_request.has_key(key) != False:
        if left_hs_first_response.has_key(key) != False:
          avg_first_request_hs += left_hs_first_response[key] - came_hs_first_request[key]
      if came_sprout_first_response.has_key(key) != False:
        if left_sprout_first_response.has_key(key) != False:
          if left_sprout_first_response[key] < came_sprout_first_response[key]:
            print "First Response - " + key + " " + str(left_sprout_first_response[key]) + " " + str(came_sprout_first_response[key])
          else:
            avg_first_response_sprout += left_sprout_first_response[key] - came_sprout_first_response[key]
      if came_bono_first_response.has_key(key) != False:
        if left_bono_first_response.has_key(key) != False:
          avg_first_response_bono += left_bono_first_response[key] - came_bono_first_response[key]
      if came_bono_second_request.has_key(key) != False:
        if left_bono_second_request.has_key(key) != False:
          avg_second_request_bono += left_bono_second_request[key] - came_bono_second_request[key]
      if came_sprout_second_request.has_key(key) != False:
        if left_sprout_second_request.has_key(key) != False:
          if left_sprout_second_request[key] < came_sprout_second_request[key]:
            print "Second Request - " + key + " " + str(left_sprout_second_request[key]) + " " + str(came_sprout_second_request[key])
          else:
            avg_second_request_sprout += left_sprout_second_request[key] - came_sprout_second_request[key]
      if came_hs_second_request.has_key(key) != False:
        if left_hs_second_response.has_key(key) != False:
          avg_second_request_hs += left_hs_second_response[key] - came_hs_second_request[key]
      if came_sprout_second_response.has_key(key) != False:
        if left_sprout_second_response.has_key(key) != False:
          if left_sprout_second_response[key] < came_sprout_second_response[key]:
            print "Second Response - " + key + " " + str(left_sprout_second_response[key]) + " " + str(came_sprout_second_response[key])
          else:
            avg_second_response_sprout += left_sprout_second_response[key] - came_sprout_second_response[key]
      if came_bono_second_response.has_key(key) != False:
        if left_bono_second_response.has_key(key) != False:
          avg_second_response_bono += left_bono_second_response[key] - came_bono_second_response[key]
    file_data.write(str(float(avg_first_request_bono)/size) + " ")
    file_data.write(str(float(avg_first_request_sprout)/size) + " ")
    file_data.write(str(float(avg_first_request_hs)/size) + " ")
    file_data.write(str(float(avg_first_response_sprout)/size) + " ")
    file_data.write(str(float(avg_first_response_bono)/size) + " ")
    file_data.write(str(float(avg_second_request_bono)/size) + " ")
    file_data.write(str(float(avg_second_request_sprout)/size) + " ")
    file_data.write(str(float(avg_second_request_hs)/size) + " ")
    file_data.write(str(float(avg_second_response_sprout)/size) + " ")
    file_data.write(str(float(avg_second_response_bono)/size) + "\n")

calculate_time_diff()
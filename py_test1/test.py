def aaa():
    throttling_list = "1,2,3"
    throttling_list = list(map(int, throttling_list.split(",")))
    #throttling_list = list((throttling_list).split(","))
    print throttling_list
    aaa = 10
    for i in range(10):
        print(aaa)
        aaa = aaa+10


aaa()
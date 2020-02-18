choice = int(input(
    "Choose Mode\n"+
    "1. Threads will restart immediately once they finish\n"+
    "2. All Threads will wait for execution completion of all threads and then restart\n"+
    "Enter Choice(1-2):"
))

aws = int(input(
    "Choose Back-end configuration:\n"+
    "1. Single Instance of Virtual Machine on AWS\n"+
    "2. 4 Instances of Virtual Machine on AWS with Load Balancer\n"+
    "3. Multiple Instances of Virtual Machine with Auto Scaling and Load Balancer\n"+
    "Enter choice(1-3):"
))
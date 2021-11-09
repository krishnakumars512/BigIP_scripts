# Tested Script for 14.1.x version
#Author -> krishnakumar S | krishna.kumas512@gmail.com

from f5.bigip import ManagementRoot
from pprint import pprint
import time
# Connect to the BigIP

host_ip=""
user_name=""
pass_word=""


mgmt = ManagementRoot(host_ip, user_name, pass_word)

# Get a list of all pools on the BigIP and print their names and their
# members' names
virtuals = mgmt.tm.ltm.virtuals.get_collection()
pools = mgmt.tm.ltm.pools.get_collection()
nodes = mgmt.tm.ltm.nodes.get_collection()

out_line=""

total_VIP_Count=0
print("Partition,Route Domain,VS_Name,VS_IP,VS_Port,VS_Status,Pool_Name,iRule,LB-Mode,Monitor,Member Server Name,Node IP,Node Port")
for virtual in virtuals:
    time.sleep(.3)
    total_VIP_Count=total_VIP_Count+1
    #print ("========VIP Start==============")
    vip_name=str(virtual.name)
    try:
        vip_temp_pool=str(virtual.pool).split("/")
        vip_pool=str(vip_temp_pool[2])
    except:
        vip_pool="N/A"
    try:
        vip_rules=str(virtual.rules)
    except:
        vip_rules="N/A"

    vip_pool=str(vip_temp_pool[2])
    vip_temp_dest01=str(virtual.destination).split("/") # Split partition and IP%rd:port
    vip_temp_dest02=str(vip_temp_dest01[2]).split(":") # Split ip%rd and port
    vip_port=str(vip_temp_dest02[1])  # -----> VIP - Port
    vip_temp_dest04=vip_temp_dest02[0].split("%")
    vip_ip=str((vip_temp_dest04[0]))
    vip_rd=str(vip_temp_dest04[1])
    vip_partition=str(vip_temp_pool[1])



    instance=1
    vip_status=str(virtual.addressStatus)
    out_line=vip_partition+","+vip_rd+","+vip_name+","+vip_ip+","+vip_port+","+vip_status+","+vip_pool+","+vip_rules
    for pool in pools:

        if (str(pool.name) == vip_pool):
            #print ("Pool Name: "+str(pool.name))


            pool_mode=str(pool.loadBalancingMode)
            pool_monitor=str(pool.monitor)


            for member in pool.members_s.get_collection():
                member_temp=str(member.name).split(":")
                mem_name=str(member_temp[0])
                mem_port=str(member_temp[1])

                for node in nodes:
                    node_name=str(node.name)
                    node_temp_01=node_name.split("%")
                    node_name=node_temp_01[0]
                    if(node_name==mem_name):
                        node_ip_temp=str(node.address).split("%")
                        node_ip=str(node_ip_temp[0])


                        if instance==1:
                            out_line=out_line+","+pool_mode+","+pool_monitor+","+str(node_name)+","+str(node_ip)+","+mem_port
                            instance=0
                            print (out_line)
                        elif instance==0:
                            out_line=",,,,,,,,,,"+str(node_name)+","+str(node_ip)+","+mem_port
                            print(out_line)

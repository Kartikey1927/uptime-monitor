# basic print 
print("web-01")

#variable declaration
server = "web-02"
print(server)

# maths operations on variable 
port = 443
cpu = 72.5
name = "web-01"

print(port + 1 )
print(cpu * 2 )
print(name + " is running")

# maths in variable situation 
total_gb = 500
used_gb = 210

free_gb = total_gb - used_gb
print(free_gb)


used_percent = (used_gb / total_gb) * 100
print(used_percent)


# maths ops 

disk_is_full = used_percent > 90
print(disk_is_full)

# if statement 
if used_percent > 90:
    print("Disk is full")
else:
    print("Disk is not full")

# else if eif situation
alert_notification = "200"
if alert_notification == "99":
    print("🔴 CRITICAL: disk almost full")
elif alert_notification == "95":
    print("🟡 WARNING: disk getting full")
elif alert_notification >= "100":
    print("🔴 CRITICAL: disk excedded")
else:
    print("🟢 OK: disk is healthy")


#one more

site_code = 100
if site_code ==200 :
    print("🟢 OK: site is healthy")
else:
    print("saab chana si")
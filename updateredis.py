__author__ = 'chiradip'
import redis
import time
import register

lua = '''
local ownuid = redis.call('GET', "username:" ..KEYS[1].. ":uid")
local issuid = redis.call('GET', "email:" ..KEYS[2].. ":uid")
if not issuid then
    issuid = redis.call('INCR', "global:getNextUserId")
    redis.call('SET', "email:" ..KEYS[2].. ":uid", issuid)
    redis.call('SET', "uid:" ..issuid.. ":email", KEYS[2])
end
redis.call('ZADD', "owner:"  ..ownuid..":docs", ARGV[1], ARGV[2])
redis.call('ZADD', "issuer:"  ..issuid..":docs", ARGV[1], ARGV[2])
redis.call('HMSET', "doc:"..ARGV[2], "owner.uid", ownuid , "issuer.uid", issuid)
print(KEYS[1] .."|".. KEYS[2] .."|".. ARGV[1] .."|".. ARGV[2])
'''
r_server = redis.Redis("localhost")
r_up = r_server.register_script(lua)

def update_redis(owner,issuer,url, dname):
  ts = time.time()
  password = "secret"
  rusername  = owner.split("@")[0]
  iusername = issuer.split("@")[0]
  idomain = issuer.split("@")[1]
  print("Before calling LUA that updates document entry for the user")
  print("Owner's email: ", owner)
  print("Issuer's email: ", issuer)
  print("Owner's user name: ", rusername)
  r_up(keys=[rusername, issuer], args=[ts,url])

  # if idomain == 'paperlessclub.org':
  #   iuid = register.get_id(iusername)
  #
  # elif register.get_by_email(issuer) is None:
  #   register.register_user(r_server, iusername, issuer, password, dname, "inactive")





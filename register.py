__author__ = 'chiradip'


def register_user(r_server, username, email, password, dname, status):
  lua = '''
  local uid = redis.call('INCR', "global:getNextUserId")

  local unamecheck_uid = redis.call('GET', "username:" ..ARGV[1].. ":uid")
  if unamecheck_uid ~= nil then error("Username Exists") end
  local emailcheck_uid = redis.call('GET', "email:" ..ARGV[2].. ":uid")
  if emailcheck_uid ~= nil then error("Email already registered") end
  redis.call('SET', "uid:" ..uid.. ":username", ARGV[1]) -- ARGV[1] is username
  redis.call('SET', "username:" ..ARGV[1].. ":uid", uid)
  redis.call('SET', "uid:" ..uid.. ":email", ARGV[2]) -- ARGV[2] is email
  redis.call('SET', "uid:" ..uid.. ":password", ARGV[3]) -- ARGV[3] is password
  redis.call('SET', "email:" ..ARGV[2].. ":uid", uid)
  redis.call('SET', "uid:" ..uid.. ":name", ARGV[4]) -- ARGV[4] is the fullname of the user
  redis.call('SET', "uid:" ..uid.. ":status", ARGV[5]) -- ARGV[5] is the status of user - active/inactive/premium etc.
  return ARGV[1] ..":".. uid ..":".. ARGV[2]
  '''
  reg = r_server.register_(lua)
  reg(keys = [], args = [username, email, password, dname, status])

def get_id(r_server, username):
  lua = '''
  -- KEYS[1] is the supplied username here
  local uid = redis.call('GET', "username:" .. KEYS[1] .. ":uid")
  local password = redis.call('GET', "uid:" ..uid.. ":password")
  local email = redis.call('GET', "uid:" ..uid.. ":email")
  local name = redis.call('GET', "uid:" ..uid.. ":name")
  local status = redis.call('GET', "uid:" ..uid.. ":status")
  print(uid .. "|" ..KEYS[1].. "|".. password .. "|" .. email.. "|" ..(name or KEYS[1]).. "|" ..(status or 'active'))
  return uid .. "|" ..KEYS[1].. "|" ..password.. "|" ..email.. "|" ..(name or KEYS[1]).. "|" ..(status or 'active')
  '''
  getid  = r_server.register(lua)
  return getid(keys = username, args = []);

def get_name(r_server, uid):
  lua = '''
  -- KEYS[1] is the supplied UID here
  local username = redis.call('GET', "uid:" ..KEYS[1].. ":username")
  local password = redis.call('GET', "uid:" ..KEYS[1].. ":password")
  local email = redis.call('GET', "uid:" ..KEYS[1].. ":email")
  local name = redis.call('GET', "uid:" ..KEYS[1].. ":name")
  local status = redis.call('GET', "uid:" ..KEYS[1].. ":status")
  print(KEYS[1].. "|" ..username.. "|" ..password.. "|" ..email.. "|" ..(name or username).. "|" ..(status or "active"))
  return KEYS[1].. "|" ..username.. "|" ..password.. "|" ..email.. "|" ..(name or username).. "|" ..(status or "active")
  '''
  getname = r_server.register(lua)
  return getname(keys = uid, args = [])

def get_by_email(r_server,email):
  lua =  '''
  '''
  getbyemail = r_server.register(lua)
  return getbyemail(keys =email, args = [])

-- KEYS[1] = key
-- ARGV[1] = limit
-- ARGV[2] = window (seconds)

local current = redis.call("GET", KEYS[1])

if current and tonumber(current) >= tonumber(ARGV[1]) then
    return 0
end

current = redis.call("INCR", KEYS[1])

if tonumber(current) == 1 then
    redis.call("EXPIRE", KEYS[1], ARGV[2])
end

return 1

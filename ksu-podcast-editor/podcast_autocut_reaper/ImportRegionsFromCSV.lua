-- ImportRegionsFromCSV.lua
local function trim(s)
  return (s:gsub("^%s+", ""):gsub("%s+$", ""))
end

local function parse_csv_line(line)
  -- Parse: start,end,"label with commas"
  local a, b, rest = line:match("^%s*([^,]+)%s*,%s*([^,]+)%s*,%s*(.+)%s*$")
  if not a or not b or not rest then return nil end
  local start_t = tonumber(trim(a))
  local end_t   = tonumber(trim(b))
  if not start_t or not end_t then return nil end
  local label = trim(rest)
  -- Remove surrounding quotes if present
  if label:sub(1,1) == '"' and label:sub(-1,-1) == '"' then
    label = label:sub(2, -2)
  end
  return start_t, end_t, label
end

local retval, path = reaper.GetUserFileNameForRead("", "Select regions CSV", "csv")
if not retval then return end

local f = io.open(path, "r")
if not f then return end

reaper.Undo_BeginBlock()
for line in f:lines() do
  local s, e, label = parse_csv_line(line)
  if s and e and e > s then
    reaper.AddProjectMarker2(0, true, s, e, label or "", -1, 0)
  end
end
f:close()
reaper.Undo_EndBlock("Import regions from CSV", -1)
reaper.UpdateArrange()

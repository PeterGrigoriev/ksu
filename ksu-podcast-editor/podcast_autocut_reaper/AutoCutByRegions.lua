-- AutoCutByRegions.lua
local CUT_PREFIXES = { "FILLER:", "REPEAT:", "CUT:" }
local PRE_PAD_SEC  = 0.10
local POST_PAD_SEC = 0.10

local function starts_with_any(name, prefixes)
  for _, p in ipairs(prefixes) do
    if name:sub(1, #p) == p then return true end
  end
  return false
end

local _, num_markers, num_regions = reaper.CountProjectMarkers(0)
local total = num_markers + num_regions
local regions = {}

for i = 0, total - 1 do
  local retval, isrgn, pos, rgnend, name = reaper.EnumProjectMarkers(i)
  if retval and isrgn and starts_with_any(name, CUT_PREFIXES) then
    table.insert(regions, {s = math.max(0, pos - PRE_PAD_SEC), e = rgnend + POST_PAD_SEC})
  end
end

table.sort(regions, function(a,b) return a.s > b.s end)

reaper.Undo_BeginBlock()
reaper.Main_OnCommand(40310, 0)

for _, r in ipairs(regions) do
  reaper.SetEditCurPos(r.s, false, false)
  reaper.Main_OnCommand(40757, 0)
  reaper.SetEditCurPos(r.e, false, false)
  reaper.Main_OnCommand(40757, 0)
  reaper.Main_OnCommand(40006, 0)
end

reaper.Main_OnCommand(40311, 0)
reaper.Undo_EndBlock("Auto-cut by regions", -1)
reaper.UpdateArrange()

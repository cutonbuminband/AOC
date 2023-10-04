--- Function called for each raw block element.
function RawBlock (raw)
  -- Don't do anything unless the block contains *org* markup.
  if raw.format ~= 'org' then return nil else return {} end
end

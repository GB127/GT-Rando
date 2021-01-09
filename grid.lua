-- "Goof Troop"
while (true) do

    for i=1,16 do
        gui.drawLine(16 * i,0, 16*i,255)
        gui.drawLine(0,16 * i, 355,16 * i)
    end

    for i=0,16 do  -- Column of the left
        gui.drawText(0,  2 + 16 * i, i, 0xFF16c6de)  -- This is for the left column
    end
    for i=1,16 do
        for j=0,16 do
            gui.drawText(16 * i,1 + 16 *j, i, 0xFFad576e)

        end
        
    end


    emu.frameadvance();
end
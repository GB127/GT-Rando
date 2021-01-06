-- "Goof Troop"
while (true) do

    for i=1,16 do
        gui.drawLine(16 * i,0, 16*i,255)
        gui.drawLine(0,16 * i, 355,16 * i)
    end

    for i=0,16 do  -- Column of the left
        gui.pixelText(5,  5 + 16 * i, i)  -- This is for the left column
    end
    for i=1,16 do
        for j=0,16 do
            gui.pixelText(1 + 16 * i,1 + 16 *j, i)

        end
        
    end


    emu.frameadvance();
end
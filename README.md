# RandomShuffler
RandomShuffler Plugin for Krita, shuffle layers positions randomly

![site under construction 2](https://user-images.githubusercontent.com/44746952/215048826-1bcbd939-60dc-4b3c-bc6f-0df7e1bc13d8.png)
![construction_done](https://user-images.githubusercontent.com/44746952/216980110-e231194b-5ad6-4151-99fc-98be6db9425e.png)


# Preview :

shuffle!
![Preview1_shuffle](https://user-images.githubusercontent.com/44746952/216971181-20aae4dd-fa93-4c22-8007-0ad20bb8305d.gif)

area_shuffle!
![Preview1_area_shuffle](https://user-images.githubusercontent.com/44746952/216971168-ff8eea41-e445-4f40-ae70-002ff8bf3506.gif)

area_shuffle! + use_non_rectangular_selection
![Preview2_non_rectangular](https://user-images.githubusercontent.com/44746952/216971193-a155fa95-f0b6-4f39-ad9a-8681f32fc156.gif)


# How to Install :
~~under construction :D !~~ construction done :> !

0. download the plugin first on this github page

![0](https://user-images.githubusercontent.com/44746952/217007123-25a114d9-9b56-48b1-96ce-a7d6411603c0.png)

1. open the Krita, click Tools > Scripts > Import Python Plugin from File

![1](https://user-images.githubusercontent.com/44746952/215260368-72ced9b1-6473-4df5-a71e-b7df3195bcfb.png)

2. locate and open the downloaded zip file

![2](https://user-images.githubusercontent.com/44746952/215260371-edf3a084-c850-4758-b027-6b481171356c.png)

3. restart the Krita (click yes, close the Krita then re-open the Krita)

![3](https://user-images.githubusercontent.com/44746952/215260375-0b069bf1-66d0-4bee-9e4f-c217321a2bf9.png)

3,5. if you aren't clicking yes, then you need to restart the Krita, enable the plugin, then restart the Krita again

![shortcut33](https://user-images.githubusercontent.com/44746952/216966714-7fba7dfe-f16c-4b2d-a5d5-cafb087a02e9.png)

![3_and_half](https://user-images.githubusercontent.com/44746952/217724086-7e18845e-b8d8-4994-93ab-b7b382fdcd0d.png)

4. go to Settings > Dockers > click Random_Shuffler

![4](https://user-images.githubusercontent.com/44746952/215260376-dead619f-b5db-4aef-89c1-26b87d34bf55.png)

5. it's ready to use :)

![5](https://user-images.githubusercontent.com/44746952/215260379-7067fc4a-61b3-4969-ab0d-294eab26675f.png)

# How to Use :
edit : see the preview above for the visuals, basically the same

--shuffle!--
1. select the layers ( at least 2 layers )
2. click shuffle!

--area_shuffle!--
1. select the layers
2. select area using RectangularSelection tool
3. click area_shuffle!

you can change the shortcut in Settings > Configure Krita > Keyboard Shorcuts > look on Scripts > RandomShuffler
current shotcut is 7 for shuffle! and 8 for area_shuffle!

![shortcut33](https://user-images.githubusercontent.com/44746952/216966714-7fba7dfe-f16c-4b2d-a5d5-cafb087a02e9.png)

![shortcut44](https://user-images.githubusercontent.com/44746952/216966724-50265243-f225-41a6-b23c-a7a969e8700f.png)


# Limitation :
1. only usable for Paint Layers type, haven't tried the others
2. area_shuffle! 2/more selection area interpreted as 1 selection area 
3. position anchor using topleft of the layers (default)
4. area_shuffle! selection : rectangular shape only (min x,y max x,y)
5. area_shuffle! use_non_rectangular_selection can't keep positions within area
6. beware! be aware : there's no undo yet so we'd better to duplicate the layers first for initial positions, (except if it doesn't matter) <----:bangbang::bangbang::bangbang:

# Updates :
V4 -- area_shuffle! use_non_rectangular_selection added

number 2 & 4 fix by V4 but the limitation is doesn't have keep_within_area yet, seem's complicated

number 1 if using vector layer, its broken goes to somewhere after some clicks, mean to be used for PaintLayer

number 3 mean as shuffle! based anchor, now using center, looks more approriate

add previews on github

# 
special thanks to all Krita developers !

alright :) !

#

edit : 9feb23 o yea i forgot to add this, so i'll add this :

maybe you need to uninstall, or retry installing, here is the procedure:

1. go to Settings > Manage Resources

![110](https://user-images.githubusercontent.com/44746952/217713129-31a648da-fed3-494e-9c29-a6413a0e6e06.png)

2. click Open Resources Folder

![111](https://user-images.githubusercontent.com/44746952/217713133-63c6ed96-c77e-46d3-a7c8-f24e90101724.png)

3. it's in these 2 folders

![111a](https://user-images.githubusercontent.com/44746952/217713136-012d4594-20f1-43e0-8687-708179e1247c.png)

4. delete these files

![111b](https://user-images.githubusercontent.com/44746952/217713140-a2c979c7-0456-4dad-9acf-67e1a6172315.png)

5. delete this one too

![111c](https://user-images.githubusercontent.com/44746952/217713127-3f7b282b-8c36-4979-afa6-3e6cfe0fdaf6.png)

done!

![ok_240x240](https://user-images.githubusercontent.com/44746952/217714559-699f3906-bed0-4d35-96b4-0ca32f03e988.png)

FYI : this was using Krita 5.1.3

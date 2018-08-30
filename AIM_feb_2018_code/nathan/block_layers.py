from ipkiss.technology import get_technology

TECH = get_technology()

#Layers on which to draw shapes surrounding optical devices to block fills
layers = [TECH.PPLAYER.AIM.BESAMFILL,
          TECH.PPLAYER.AIM.BCAAMFILL,
          TECH.PPLAYER.AIM.BSEAMFILL,
          TECH.PPLAYER.AIM.BFNAMFILL,
          TECH.PPLAYER.AIM.BSNAMFILL,
          TECH.PPLAYER.AIM.BM1AMFILL,
          TECH.PPLAYER.AIM.BM2AMFILL,
          TECH.PPLAYER.AIM.BMLAMFILL]
#Extra distance from optical device edges to edges of bfill shapes
widths = (4.0,
               4.0,
               4.0,
               4.0,
               4.0,
               4.0,
               4.0,
               4.0)
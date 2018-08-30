############################################################################################
# Layer setting:
# 
# This file defines the process layer and purpose layers
# # Extra layers and purposes are defined for IPKISS, IPKISS.eda and PICAZZO usage (see comment)
############################################################################################

from ipkiss.technology.technology import ProcessTechnologyTree, TechnologyTree
from ipkiss.process.layer import ProcessLayer
from ipkiss.technology import get_technology

TECH = get_technology()

#################
# Process layers
#################

TECH.PROCESS = ProcessTechnologyTree()

# FEOL
# SOI/poly patterning
TECH.PROCESS.WG = ProcessLayer(name="Strip waveguides (full etched SOI)", extension="WG")
TECH.PROCESS.FC = ProcessLayer(name="Fiber couplers and rib waveguides (shallow partial etched SOI)", extension="FC")
TECH.PROCESS.SKT = ProcessLayer(name="Socket waveguides (deep partial etched SOI)", extension="SKT")
TECH.PROCESS.FCW = ProcessLayer(name="Fiber coupler window (poly)", extension="FCW")

# Implants
TECH.PROCESS.NBODY = ProcessLayer(name="N-type Body implant", extension="NBODY")
TECH.PROCESS.PBODY = ProcessLayer(name="P-type Body implant" , extension="PBODY")
TECH.PROCESS.N1 = ProcessLayer(name="N-type implant - dose 1", extension="N1")
TECH.PROCESS.N2 = ProcessLayer(name="N-type implant - dose 2", extension="N2")
TECH.PROCESS.NPLUS = ProcessLayer(name="N-type contact implant" , extension="NPLUS")
TECH.PROCESS.P1 = ProcessLayer(name="P-type implant - dose 1", extension="P1")
TECH.PROCESS.P2 = ProcessLayer(name="P-type implant - dose 2", extension="P2")
TECH.PROCESS.PPLUS = ProcessLayer(name="P-type contact implant", extension="PPLUS")

# silicide and contact
TECH.PROCESS.SAL = ProcessLayer("Local Silicide","SAL")
TECH.PROCESS.PCON = ProcessLayer("Tungsten Contact Plugs","PCON")

# metal
TECH.PROCESS.M1 = ProcessLayer("Metal1 1" ,"M1")
TECH.PROCESS.VIA12 = ProcessLayer("M1 to M2 Via" ,"VIA12")
TECH.PROCESS.M2 = ProcessLayer("Metal1 2" ,"M2")
TECH.PROCESS.PASS1 = ProcessLayer("Windows in passivation nitride", "PASS1")
TECH.PROCESS.METPASS = ProcessLayer("Al bond pads", "METPASS")

# BEOL
TECH.PROCESS.EXPO = ProcessLayer("BEOL etch for waveguide exposure", "EXPO")
TECH.PROCESS.LPASS = ProcessLayer("BEOL etch for grating couplers and edge couplers", "LPASS")
TECH.PROCESS.PASS2 = ProcessLayer("Open passivation on bond pads", "PASS2")
TECH.PROCESS.TRENCH = ProcessLayer("Deep trench","TRENCH")

# Auxiliary
TECH.PROCESS.NONE = ProcessLayer(name="No specific process", extension="NONE")

###########################
# Drawing pattern purposes
###########################

from ipkiss.process.layer import PatternPurpose
TECH.PURPOSE = TechnologyTree()
# actual mask drawings
TECH.PURPOSE.DRAWING = PatternPurpose(name="Drawing", extension="DRAWING")
TECH.PURPOSE.CORE = PatternPurpose(name="Waveguide core", extension="COR")
TECH.PURPOSE.CLADDING = PatternPurpose(name="Waveguide cladding", extension="CLD")
TECH.PURPOSE.TRENCH = PatternPurpose(name="Etched trench (linear)", extension="TRE")
TECH.PURPOSE.HOLE = PatternPurpose(name="Etched hole (polygon)", extension="HOL")
TECH.PURPOSE.INVERSION = PatternPurpose(name = "Inversion", extension = "INV")
# ipkiss defined keys
TECH.PURPOSE.LF = TechnologyTree()
TECH.PURPOSE.DF = TechnologyTree()
TECH.PURPOSE.LF_AREA = PatternPurpose(name="Light-field area", extension="LFAREA")
TECH.PURPOSE.DF_AREA = PatternPurpose(name="Dark-field area", extension="DFAREA")
TECH.PURPOSE.LF.LINE = PatternPurpose(name="Light-field line", extension="LFLINE")
TECH.PURPOSE.DF.LINE = PatternPurpose(name="Dark-field line", extension="DFLINE")
TECH.PURPOSE.DF.POLYGON = PatternPurpose(name="Dark-field polygon", extension="POLYGON")
# auxiliary data
TECH.PURPOSE.ERROR = PatternPurpose(name="ERROR", extension = "ERROR")
TECH.PURPOSE.PERF = PatternPurpose(name = "Metal perforation", extension = "PERF")
TECH.PURPOSE.NO_PERF = PatternPurpose(name = "No metal perforation", extension = "NOPERF")
TECH.PURPOSE.INVISIBLE = PatternPurpose(name = "Invisible", extension = "INVIS")
TECH.PURPOSE.OPT_DUM = PatternPurpose(name = "Dummy cells in optical layers (WG body, polysilicon and Ge)", extension = "OPT_DUM")
TECH.PURPOSE.LOGOTXT = PatternPurpose(name = "Text and logo on WG and M1", extension = "LOGOTXT")
TECH.PURPOSE.NOMET = PatternPurpose(name = "No metal", extension = "NOMET")
TECH.PURPOSE.NOFILL = PatternPurpose(name = "No tiling", extension = "NOFILL")
TECH.PURPOSE.VERTBX = PatternPurpose(name = "Vertical port indication", extension = "VERTBX")
TECH.PURPOSE.DICING = PatternPurpose(name = "Dicing street", extension = "DICING")
TECH.PURPOSE.DOC = PatternPurpose(name = "Other documentation information", extension = "DOC")
TECH.PURPOSE.IP = PatternPurpose(name = "IP box", extension = "IP")
TECH.PURPOSE.LABEL = PatternPurpose(name = "Device label", extension = "LABEL")
TECH.PURPOSE.PIN = PatternPurpose(name = "PIN", extension = "PIN")
TECH.PURPOSE.PAYLOAD = PatternPurpose(name = "Outline of design block", extension = "PAYLOAD")
#required by PICAZZO
TECH.PURPOSE.TEXT = TECH.PURPOSE.LOGOTXT
TECH.PURPOSE.TRACE = PatternPurpose(name = "Trace of waveguide template", extension = "TRACE")
TECH.PURPOSE.BBOX = PatternPurpose(name = "Bounding Box", extension = "BBOX")

# CHANGES FOR AIM (bz)

TECH.PURPOSE.BESAMFILL = PatternPurpose(name = "BESAMFILL", extension = "BESAMFILL")
TECH.PURPOSE.BCAAMFILL = PatternPurpose(name = "BCAAMFILL", extension = "BCAAMFILL")
TECH.PURPOSE.BSEAMFILL = PatternPurpose(name = "BSEAMFILL", extension = "BSEAMFILL")
TECH.PURPOSE.BFNAMFILL = PatternPurpose(name = "BFNAMFILL", extension = "BFNAMFILL")
TECH.PURPOSE.BSNAMFILL = PatternPurpose(name = "BSNAMFILL", extension = "BSNAMFILL")
TECH.PURPOSE.BM1AMFILL = PatternPurpose(name = "BM1AMFILL", extension = "BM1AMFILL")
TECH.PURPOSE.BM1AMCHE = PatternPurpose(name = "BM1AMCHE", extension = "BM1AMCHE")
TECH.PURPOSE.BMLAMFILL = PatternPurpose(name = "BMLAMFILL", extension = "BMLAMFILL")
TECH.PURPOSE.BM2AMFILL = PatternPurpose(name = "BM2AMFILL", extension = "BM2AMFILL")
TECH.PURPOSE.BM2AMCHE = PatternPurpose(name = "BM2AMCHE", extension = "BM2AMCHE")
TECH.PURPOSE.BMLAMCHE = PatternPurpose(name = "BMLAMCHE", extension = "BMLAMCHE")

TECH.PURPOSE.WGKOAM = PatternPurpose(name = "WGKOAM", extension = "WGKOAM")
TECH.PURPOSE.METKOAM= PatternPurpose(name = "METKOAM", extension = "METKOAM")
TECH.PURPOSE.ABSTRACTAM= PatternPurpose(name = "ABSTRACTAM", extension = "ABSTRACTAM")
TECH.PURPOSE.LOGOAM= PatternPurpose(name = "LOGOAM", extension = "LOGOAM")
TECH.PURPOSE.LOGO2AM= PatternPurpose(name = "LOGO2AM", extension = "LOGO2AM")

TECH.PURPOSE.ZLAM= PatternPurpose(name = "ZLAM", extension = "ZLAM")
TECH.PURPOSE.REAM= PatternPurpose(name = "REAM", extension = "REAM")
TECH.PURPOSE.SEAM= PatternPurpose(name = "SEAM", extension = "SEAM")
TECH.PURPOSE.ENAM= PatternPurpose(name = "ENAM", extension = "ENAM")
TECH.PURPOSE.FNAM= PatternPurpose(name = "FNAM", extension = "FNAM")
TECH.PURPOSE.SNAM= PatternPurpose(name = "SNAM", extension = "SNAM")
TECH.PURPOSE.NDAM= PatternPurpose(name = "NDAM", extension = "NDAM")
TECH.PURPOSE.NNAM= PatternPurpose(name = "NNAM", extension = "NNAM")
TECH.PURPOSE.NNNAM= PatternPurpose(name = "NNNAM", extension = "NNNAM")
TECH.PURPOSE.PDAM= PatternPurpose(name = "PDAM", extension = "PDAM")
TECH.PURPOSE.PPAM= PatternPurpose(name = "PPAM", extension = "PPAM")
TECH.PURPOSE.PPPAM= PatternPurpose(name = "PPPAM", extension = "PPPAM")

TECH.PURPOSE.TRAM= PatternPurpose(name = "TRAM", extension = "TRAM")
TECH.PURPOSE.NGAM= PatternPurpose(name = "NGAM", extension = "NGAM")
TECH.PURPOSE.ESAM= PatternPurpose(name = "ESAM", extension = "ESAM")
TECH.PURPOSE.CAAM= PatternPurpose(name = "CAAM", extension = "CAAM")
TECH.PURPOSE.CBAM= PatternPurpose(name = "CBAM", extension = "CBAM")
TECH.PURPOSE.M1AM= PatternPurpose(name = "M1AM", extension = "M1AM")
TECH.PURPOSE.V1AM= PatternPurpose(name = "V1AM", extension = "V1AM")
TECH.PURPOSE.M2AM= PatternPurpose(name = "M2AM", extension = "M2AM")
TECH.PURPOSE.VAAM= PatternPurpose(name = "VAAM", extension = "VAAM")
TECH.PURPOSE.MLAM= PatternPurpose(name = "MLAM", extension = "MLAM")
TECH.PURPOSE.DIAM= PatternPurpose(name = "DIAM", extension = "DIAM")
TECH.PURPOSE.PAAM= PatternPurpose(name = "PAAM", extension = "PAAM")

TECH.PURPOSE.LOL709 = PatternPurpose(name = "whatever man", extension = "LOL709")
TECH.PURPOSE.LOL804 = PatternPurpose(name = "whatever man 804", extension = "LOL804")
TECH.PURPOSE.LOL7090 = PatternPurpose(name = "whatever man 709 0", extension = "LOL7090")
TECH.PURPOSE.LOL7250 = PatternPurpose(name = "whatever man 709 0", extension = "LOL7250")

# END CHANGES FOR AIM

########################
# Process-Purpose layers
########################


from ipkiss.process.layer import PPLayer
TECH.PPLAYER = TechnologyTree()

### SI: full SOI etch ###
# CHANGES FOR AIM PHOTONICS BEGIN HERE!!!!!!!!!!!!!!!
TECH.PPLAYER.WG = TechnologyTree()
TECH.PPLAYER.WG.COR = PPLayer(TECH.PROCESS.WG, TECH.PURPOSE.CORE, name="SEAM")
TECH.PPLAYER.WG.CLD = PPLayer(TECH.PROCESS.WG, TECH.PURPOSE.CLADDING, name="BSEAMFILL")
TECH.PPLAYER.WG.TRE = PPLayer(TECH.PROCESS.WG, TECH.PURPOSE.TRENCH, name="REAM")
TECH.PPLAYER.WG.HOL   = PPLayer(TECH.PROCESS.WG, TECH.PURPOSE.HOLE, name="REAM")
# CHANGES END (MORE LATER)

### FC: 70nm SOI etch ###
TECH.PPLAYER.FC = TechnologyTree()
TECH.PPLAYER.FC.COR = PPLayer(TECH.PROCESS.FC, TECH.PURPOSE.CORE, name="FC_COR")
TECH.PPLAYER.FC.CLD = PPLayer(TECH.PROCESS.FC, TECH.PURPOSE.CLADDING, name="FC_CLD")
TECH.PPLAYER.FC.TRE = PPLayer(TECH.PROCESS.FC, TECH.PURPOSE.TRENCH, name="FC_TRE")
TECH.PPLAYER.FC.HOL = PPLayer(TECH.PROCESS.FC, TECH.PURPOSE.HOLE, name="FC_HOL")

### SKT: 160nm SOI etch ###
TECH.PPLAYER.SKT = TechnologyTree()
TECH.PPLAYER.SKT.COR = PPLayer(TECH.PROCESS.SKT, TECH.PURPOSE.CORE, name="SKT_COR")
TECH.PPLAYER.SKT.CLD = PPLayer(TECH.PROCESS.SKT, TECH.PURPOSE.CLADDING, name="SKT_CLD")
TECH.PPLAYER.SKT.TRE = PPLayer(TECH.PROCESS.SKT, TECH.PURPOSE.TRENCH, name="SKT_TRE")
TECH.PPLAYER.SKT.HOL = PPLayer(TECH.PROCESS.SKT, TECH.PURPOSE.HOLE, name="SKT_HOL")

### FCW: 160nm poly etch ###
TECH.PPLAYER.FCW = TechnologyTree()
TECH.PPLAYER.FCW.COR = PPLayer(TECH.PROCESS.FCW, TECH.PURPOSE.CORE, name="FCW_COR")
TECH.PPLAYER.FCW.TRE = PPLayer(TECH.PROCESS.FCW, TECH.PURPOSE.TRENCH, name="FCW_TRE")
TECH.PPLAYER.FCW.INV = PPLayer(TECH.PROCESS.FCW, TECH.PURPOSE.INVERSION, name="FCW_INV")

### Implants: NBODY, PBODY, N1, P1, N2, P2, NPLUS, PPLUS###
TECH.PPLAYER.NBODY = TechnologyTree()
TECH.PPLAYER.NBODY.DRAWING = PPLayer(process=TECH.PROCESS.NBODY, purpose=TECH.PURPOSE.DRAWING, name="NBODY")

TECH.PPLAYER.PBODY = TechnologyTree()
TECH.PPLAYER.PBODY.DRAWING = PPLayer(process=TECH.PROCESS.PBODY, purpose=TECH.PURPOSE.DRAWING, name="PBODY")

TECH.PPLAYER.N1 = TechnologyTree()
TECH.PPLAYER.N1.DRAWING = PPLayer(process=TECH.PROCESS.N1, purpose=TECH.PURPOSE.DRAWING, name="N1")

TECH.PPLAYER.P1 = TechnologyTree()
TECH.PPLAYER.P1.DRAWING = PPLayer(process=TECH.PROCESS.P1, purpose=TECH.PURPOSE.DRAWING, name="P1")

TECH.PPLAYER.N2 = TechnologyTree()
TECH.PPLAYER.N2.DRAWING = PPLayer(process = TECH.PROCESS.N2, purpose = TECH.PURPOSE.DRAWING,name="N2")

TECH.PPLAYER.P2 = TechnologyTree()
TECH.PPLAYER.P2.DRAWING = PPLayer(process = TECH.PROCESS.P2, purpose = TECH.PURPOSE.DRAWING,name="P2")

TECH.PPLAYER.NPLUS = TechnologyTree()
TECH.PPLAYER.NPLUS.DRAWING = PPLayer(process=TECH.PROCESS.NPLUS, purpose=TECH.PURPOSE.DRAWING, name="NPLUS")

TECH.PPLAYER.PPLUS = TechnologyTree()
TECH.PPLAYER.PPLUS.DRAWING = PPLayer(process=TECH.PROCESS.PPLUS, purpose=TECH.PURPOSE.DRAWING, name="PPLUS")

### Salicide: SAL ###
TECH.PPLAYER.SAL = TechnologyTree()
TECH.PPLAYER.SAL.DRAWING = PPLayer(process = TECH.PROCESS.SAL, purpose = TECH.PURPOSE.DRAWING,name="SAL")

TECH.PPLAYER.PCON = TechnologyTree()
TECH.PPLAYER.PCON.DRAWING = PPLayer(process = TECH.PROCESS.PCON, purpose = TECH.PURPOSE.DRAWING,name="PCON")

### Metal 1: M1 ###
TECH.PPLAYER.M1 = TechnologyTree()
TECH.PPLAYER.M1.DRAWING = PPLayer(TECH.PROCESS.M1, purpose = TECH.PURPOSE.DRAWING,name="M1_DRW")
TECH.PPLAYER.M1.NOFILL = PPLayer(TECH.PROCESS.M1, TECH.PURPOSE.NOFILL, name="M1_NOFILL")
TECH.PPLAYER.M1.PERF = PPLayer(TECH.PROCESS.M1, TECH.PURPOSE.PERF, name = "M1_PERF")
TECH.PPLAYER.M1.NOPERF = PPLayer(TECH.PROCESS.M1, purpose = TECH.PURPOSE.NO_PERF, name="M1_NOPERF")

### Contacts (M1 and M2): VIA12 ###
TECH.PPLAYER.VIA12 = TechnologyTree()
TECH.PPLAYER.VIA12.DRAWING = PPLayer(process = TECH.PROCESS.VIA12, purpose = TECH.PURPOSE.DRAWING,name="VIA12")

### Metal 2: M2 ###
TECH.PPLAYER.M2 = TechnologyTree()
TECH.PPLAYER.M2.DRAWING = PPLayer(TECH.PROCESS.M2, TECH.PURPOSE.DRAWING,name="M2_DRW")
TECH.PPLAYER.M2.NOFILL = PPLayer(TECH.PROCESS.M2, TECH.PURPOSE.NOFILL, name="M2_NOFILL")
TECH.PPLAYER.M2.PERF = PPLayer(TECH.PROCESS.M2, TECH.PURPOSE.PERF, name = "M2_PERF")
TECH.PPLAYER.M2.NOPERF = PPLayer(TECH.PROCESS.M2, TECH.PURPOSE.NO_PERF, name="M2_NOPERF")

### Pads and passivation: PASS1/METPASS ###
TECH.PPLAYER.PASS1 = TechnologyTree()
TECH.PPLAYER.PASS1.DRAWING = PPLayer(TECH.PROCESS.PASS1, TECH.PURPOSE.DRAWING,name="PASS1")

TECH.PPLAYER.METPASS = TechnologyTree()
TECH.PPLAYER.METPASS.DRAWING = PPLayer(TECH.PROCESS.METPASS, TECH.PURPOSE.DRAWING,name="METPASS")

### Back-end opening: EXPO ###
TECH.PPLAYER.EXPO = TechnologyTree()
TECH.PPLAYER.EXPO.DRAWING = PPLayer(TECH.PROCESS.EXPO, TECH.PURPOSE.DRAWING, name="EXPO")

### Passivation opening for fiber couplers: LPASS2 ###
TECH.PPLAYER.LPASS = TechnologyTree()
TECH.PPLAYER.LPASS.DRAWING = PPLayer(TECH.PROCESS.LPASS, TECH.PURPOSE.DRAWING,name="LPASS")

### Pads and passivation: PASS2 ###
TECH.PPLAYER.PASS2 = TechnologyTree()
TECH.PPLAYER.PASS2.DRAWING = PPLayer(TECH.PROCESS.PASS2, TECH.PURPOSE.DRAWING,name="PASS2")

### Deep Si etch: TRE ###
TECH.PPLAYER.TRE = TechnologyTree()
TECH.PPLAYER.TRE.DRAWING = PPLayer(TECH.PROCESS.TRENCH, TECH.PURPOSE.DRAWING,name="TRENCH")

### Auxiliary layers: None ###
#MORE CHANGES FOR AIM
TECH.PPLAYER.NONE = TechnologyTree()
TECH.PPLAYER.NONE.OPT_DUM = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.OPT_DUM, name="ABSTRACTAM")
TECH.PPLAYER.NONE.LOGOTXT = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.LOGOTXT, name="ABSTRACTAM")
TECH.PPLAYER.NONE.NOMET = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.NOMET, name="NOMET")
TECH.PPLAYER.NONE.NOFILL = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.NOFILL, name="NOFILL")
TECH.PPLAYER.NONE.VERTBX = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.VERTBX, name="VERTBX")
TECH.PPLAYER.NONE.DICING = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.DICING, name="DICING")
TECH.PPLAYER.NONE.DOC = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.DOC, name="ABSTRACTAM")
TECH.PPLAYER.NONE.IP = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.IP, name="IP")
TECH.PPLAYER.NONE.LABEL = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.LABEL, name="ABSTRACTAM")
TECH.PPLAYER.NONE.PIN = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.PIN, name="ABSTRACTAM")
TECH.PPLAYER.NONE.PAYLOAD = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.PAYLOAD, name="PAYLOAD_DRW")

# AIM LAYERS
TECH.PPLAYER.AIM = TechnologyTree()
TECH.PPLAYER.AIM.BESAMFILL = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.BESAMFILL, name="BESAMFILL")
TECH.PPLAYER.AIM.BCAAMFILL = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.BCAAMFILL, name="BCAAMFILL")
TECH.PPLAYER.AIM.BSEAMFILL = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.BSEAMFILL, name="BSEAMFILL")
TECH.PPLAYER.AIM.BFNAMFILL = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.BFNAMFILL, name="BFNAMFILL")
TECH.PPLAYER.AIM.BSNAMFILL = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.BSNAMFILL, name="BSNAMFILL")
TECH.PPLAYER.AIM.BM1AMFILL = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.BM1AMFILL, name="BM1AMFILL")
TECH.PPLAYER.AIM.BMLAMFILL = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.BMLAMFILL, name="BMLAMFILL")
TECH.PPLAYER.AIM.BM2AMFILL = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.BM2AMFILL, name="BM2AMFILL")
TECH.PPLAYER.AIM.FNAM      = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.FNAM,      name="FNAM")            # bottom nitride layer
TECH.PPLAYER.AIM.SNAM      = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.SNAM,      name="SNAM")            # top nitride layer

#CHANGES END

# required tech keys for Ipkiss compatibility
TECH.PPLAYER.WG.TEXT = TECH.PPLAYER.NONE.LOGOTXT

TECH.PPLAYER.M1.LINE = TECH.PPLAYER.M1.DRAWING
TECH.PPLAYER.M2.LINE = TECH.PPLAYER.M2.DRAWING
TECH.PPLAYER.V12 = TechnologyTree()
TECH.PPLAYER.V12.PILLAR = TECH.PPLAYER.VIA12

TECH.PROCESS.SK = TechnologyTree()
TECH.PROCESS.SK.COR = TECH.PPLAYER.SKT.COR
TECH.PROCESS.SK.CLD = TECH.PPLAYER.SKT.CLD

# required for Ipkiss.eda compatibility
TECH.PPLAYER.WG.TRACE = PPLayer(TECH.PROCESS.WG,TECH.PURPOSE.TRACE,name="WG_TRACE")
TECH.PPLAYER.FC.TRACE = PPLayer(TECH.PROCESS.FC,TECH.PURPOSE.TRACE,name="FC_TRACE")
TECH.PPLAYER.SKT.TRACE = PPLayer(TECH.PROCESS.SKT,TECH.PURPOSE.TRACE,name="SKT_TRACE")

# required for Picazzo
TECH.PPLAYER.ERROR  = TechnologyTree()
TECH.PPLAYER.ERROR.GENERIC = PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.ERROR, name="ERROR")
TECH.PPLAYER.ERROR.CROSSING = TECH.PPLAYER.ERROR.GENERIC

TECH.PPLAYER.NONE.BBOX = PPLayer(process=TECH.PROCESS.NONE, purpose = TECH.PURPOSE.BBOX,name="BBOX")

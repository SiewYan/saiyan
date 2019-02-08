import uproot, uproot_methods
import numpy as np
from Builder import Initialize

file = uproot.open("nano_5.root")
tree = file["Events"]

####
# Object Initialization
###

'''
met_trigger_paths = ["HLT_PFMET170_NoiseCleaned",
            "HLT_PFMET170_HBHECleaned",
            "HLT_PFMET170_JetIdCleaned",
            "HLT_PFMET170_NotCleaned",
            #"HLT_PFMET170_HBHE_BeamHaloCleaned",
            #"HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight",
            #"HLT_PFMETNoMu110_NoiseCleaned_PFMHTNoMu110_IDTight",
            #"HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight",
            "HLT_PFMETNoMu90_PFMHTNoMu90_IDTight",
            "HLT_PFMETNoMu100_PFMHTNoMu100_IDTight",
            "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight"]
met_trigger = {path:tree.array(path) for path in met_trigger_paths}

event = Initialize({'isMET':np.prod([met_trigger[key] for key in met_trigger_paths], axis=0)
                    'lhe':tree.array('thefuckinglheweight')})

xsec = parse_xsec(cfgfile)[dataset_name]
event["xsecweight"], event["scaleweight"], event["pdfweight"] = calculate_xsec_weights(len(Events), xsec, Events.lhe, lumi=1000.)
'''

e = Initialize({'pt':tree.array("Electron_pt"),
                'eta':tree.array("Electron_eta"),
                'phi':tree.array("Electron_phi"),
                'mass':tree.array("Electron_mass"),
                'iso':tree.array('Electron_pfRelIso03_all'),
                'dxy':tree.array('Electron_dxy'),
                'dz':tree.array('Electron_dz'),
                'loose_id':tree.array('Electron_mvaSpring16GP_WP90'),
                'tight_id':tree.array('Electron_mvaSpring16GP_WP80')})
e['isloose'] = (e.pt>7)&(abs(e.eta)<2.4)&(abs(e.dxy)<0.05)&(abs(e.dz)<0.2)&(e.iso<0.4)&(e.loose_id)
e['istight'] = (e.pt>30)&(abs(e.eta)<2.4)&(abs(e.dxy)<0.05)&(abs(e.dz)<0.2)&(e.tight_id)&(e.iso<0.06)
e_loose = e[e.isloose]
e_tight = e[e.istight]
e_ntot = e.counts
e_nloose = e_loose.counts
e_ntight = e[e.istight].counts

mu = Initialize({'pt':tree.array("Muon_pt"),
                 'eta':tree.array("Muon_eta"),
                 'phi':tree.array("Muon_phi"),
                 'mass':tree.array("Muon_mass"),
                 'iso':tree.array('Muon_pfRelIso04_all'),
                 'dxy':tree.array('Muon_dxy'),
                 'dz':tree.array('Muon_dz')})
mu['isloose']=(mu.counts>0)&(mu.pt>5)&(abs(mu.eta)<2.4)&(abs(mu.dxy)<0.5)&(abs(mu.dz)<1.0)&(mu.iso<0.4)
m_loose=mu[mu.isloose]
mu_ntot = mu.counts
mu_nloose = m_loose.counts

tau = Initialize({'pt':tree.array('Tau_pt'),
                  'eta':tree.array('Tau_eta'),
                  'phi':tree.array('Tau_phi'),
                  'mass':tree.array('Tau_mass'),
                  'decayMode':tree.array('Tau_idDecayMode'),
                  'decayModeNew':tree.array('Tau_idDecayModeNewDMs'),
                  'id':tree.array('Tau_idMVAnew')})
tau['isloose']=(tau.counts>0)&(tau.pt>18)&(abs(tau.eta)<2.3)&(tau.decayMode)&((tau.id&2)!=0)
tau_loose=tau[tau.isloose]
tau_ntot=tau.counts
tau_nloose=tau_loose.counts

pho = Initialize({'pt':tree.array('Photon_pt'),
                 'eta':tree.array('Photon_eta'),
                 'phi':tree.array('Photon_phi'),
                 'mass':tree.array('Photon_mass')})
pho['isloose'] = (pho.counts>0)&(pho.pt>15)*(abs(pho.eta)<2.5)
pho_loose=pho[pho.isloose]
pho_ntot=pho.counts
pho_nloose=pho_loose.counts

fj = Initialize({'pt':tree.array('AK15Puppi_pt'),
                 'eta':tree.array('AK15Puppi_eta'),
                 'phi':tree.array('AK15Puppi_phi'),
                 'mass':tree.array('AK15Puppi_mass'),
                 'jetId':tree.array('AK15Puppi_jetId')})
fj['isgood'] = (fj.pt > 200)&(abs(fj.eta)<2.4)&(fj.jetId > 0)
fj['isclean'] =~fj.match(pho,1.5)&~fj.match(mu,1.5)&~fj.match(e,1.5)&fj.isgood
fj_good=fj[fj.isgood]
fj_clean=fj[fj.isclean]
fj_ntot=fj.counts
fj_ngood=fj_good.counts
fj_nclean=fj_clean.counts

j = Initialize({'pt':tree.array('Jet_pt'),
                'eta':tree.array('Jet_eta'),
                'phi':tree.array('Jet_phi'),
                'mass':tree.array('Jet_mass'),
                'id':tree.array('Jet_jetId')})
j['isgood'] = (j.pt>25)&(abs(j.eta)<4.5)&((j.id&2)!=0)
j['isclean'] = ~j.match(e,0.4)&~j.match(mu,0.4)&~j.match(pho,0.4)&j.isgood
j['isiso'] =  ~(j.match(fj,1.5))&j.isclean
j_good = j[j.isgood]
j_clean = j[j.isclean]
j_iso = j[j.isiso]
j_ntot=j.counts
j_ngood=j_good.counts
j_nclean=j_clean.counts
j_niso=j_iso.counts

met = Initialize({'pt':tree.array("MET_pt"),
                  'eta':0,
                  'phi':tree.array("MET_phi"),
                  'mass':0})

diele = e_loose.distincts().i0+e_loose.distincts().i1
dimu = m_loose.distincts().i0+m_loose.distincts().i1
uwm = met+m_loose
uwe = met+e_loose
uzmm = met+dimu
uzee = met+diele
upho = met+pho_loose

skinny = (j_nclean>0)
loose = (fj_nclean>0)
zeroL = (e_nloose==0)&(mu_nloose==0)&(tau_nloose==0)&(pho_nloose==0)
oneM = (e_nloose==0)&(mu_nloose==1)&(tau_nloose==0)&(pho_nloose==0)
oneE = (e_nloose==1)&(mu_nloose==0)&(tau_nloose==0)&(pho_nloose==0)
twoM = (e_nloose==0)&(mu_nloose==2)&(tau_nloose==0)&(pho_nloose==0)
twoE = (e_nloose==2)&(mu_nloose==0)&(tau_nloose==0)&(pho_nloose==0)
oneA = (e_nloose==0)&(mu_nloose==0)&(tau_nloose==0)&(pho_nloose==1)

sr = (j_clean[zeroL&skinny,0].pt>100)&(met[zeroL&skinny].pt>200)&(met[zeroL&skinny].delta_phi(met[zeroL&skinny].closest(j_clean[zeroL&skinny]))>0.5)
#sr = (j[j.isclean][skinny&zeroL,0].pt>100)
#print(e[e.isloose][e_nloose==1])
#print(met._hasjagged())
#print(diele[e_ntot==1].pt>0)
#print(uwm[mu.counts==1].pt)
print(sr)

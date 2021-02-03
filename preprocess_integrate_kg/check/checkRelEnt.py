import pickle

cnpt = "/home/yujin/dot/preprocess_integrate_kg/data/conceptnet/relation_vocab.pkl"

dokg = "/home/yujin/dot/preprocess_integrate_kg/data/dokg/relation_vocab.pkl"


with open(cnpt, 'rb') as handle:
    cnpt_rels = pickle.load(handle)

with open(dokg, 'rb') as handle:
    dokg_rels = pickle.load(handle)

print("**************conceptNet**************")
print(len(cnpt_rels['i2r']))
print(cnpt_rels['i2r'])
print("**************dokg**************")
print(len(dokg_rels['i2r']))
print(dokg_rels['i2r'])
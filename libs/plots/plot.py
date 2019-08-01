import matplotlib.pyplot as plt

weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
actual = [1, 2, 3, 4, 7, 10, 8, 9, 11, 13]
lin1 = [1, 2, 3, 4, 5, 7, 8, 9, 11, 12]
lin2 = [1, 2, 3, 4, 5, 6, 8, 10, 12, 13]
lin3 = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14]

rid1 = [1, 2, 3, 4, 5, 7, 8, 9, 11, 12]
rid2 = [1, 2, 3, 4, 5, 7, 8, 9, 11, 12]
rid3 = [1, 2, 3, 4, 5, 7, 9, 10, 12, 14]

mae11 = [0, 1.193408087579079, 1.953983201010935, 2.62882996267319, 3.133577681452692, 3.5230108575759904, 3.829489699495981, 4.152486153596407]
mae12 = [0, 1.1880483736879617, 1.892166694590595, 2.3149290257146027, 2.845168637153434, 3.223599112186446, 3.4462184551881294, 3.7159954981778047]
mae21 = [0, 1.2008556167473505, 1.7552165457926252, 2.504876177931064, 2.986865417033023, 3.4218650918677493, 3.733156596458415, 3.84741453104074]
mae22 = [0, 1.1266919549380194, 1.7664125520937968, 2.2066022181286984, 2.63787337712548, 3.1635725749579646, 3.3899981641277113, 3.6155850186146945] # w ridge

weeks = weeks[2:]

plt.plot(weeks, mae11, color='r', label="(1, 1)")
plt.plot(weeks, mae12, color='y', label="(1, 2)")
plt.plot(weeks, mae21, color='g', label="(2, 1)")
plt.plot(weeks, mae22, color='b', label="(2, 2)")

#plt.plot(weeks, lin1, color='r', label="Past Rank")
#plt.plot(weeks, lin2, color='y', label="Past Rank & Genre")
#plt.plot(weeks, lin3, color='g', label="Past Rank, Genre, Google Trends")
#plt.plot(weeks, actual, color='b', label="Actual")
#plt.title("Quadratic Ridge Regression Prediction (ISBN: 0525952926, Winter of the World)", fontsize=10)
plt.xlabel("Week")
plt.ylabel("MAE")
#plt.gca().set_ylim([0, 20])
#plt.gca().invert_yaxis()
plt.legend()
plt.show()
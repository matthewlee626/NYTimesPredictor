import matplotlib.pyplot as plt

mae_past = [1.1266666666666667, 1.86, 2.6866666666666665, 3.18, 3.3933333333333335, 3.8066666666666666, 4.093333333333334]
mae_past_quad = [1.6019417475728155, 2.1650485436893203, 2.6553398058252426, 2.995145631067961, 3.2184466019417477, 3.7184466019417477, 4.155339805825243]
mae_past_hybrid = [1.7087378640776698, 2.3640776699029127, 2.8689320388349513, 3.3009708737864076, 3.4514563106796117, 3.8932038834951457, 4.228155339805825]
mae_past_genre = [1.1675603620087671, 1.8965813490833474, 2.6204116791793473, 3.131752196597229, 3.366870363857501, 3.739248128640714, 4.040943562791327]
mae_past_genre_quad = [1.1362260208943633, 1.7874614532877384, 2.344265721380022, 2.7746239228606933, 3.16955463253803, 3.414009181909546, 3.894020633732492]
mae_past_genre_hybrid = [1.166461002525649, 1.8123840406338096, 2.593780403960814, 3.0708494481989215, 3.366793465189161, 3.755326754624854, 4.059174259728522]
dif = []

#past, no genre
fiction_actual = [1, 2, 3, 3, 5, 4, 4, 7, 16, 15]
fiction_predicted = [1, 2, 3, 4, 5, 7, 8, 9, 11, 12]
nonfiction_actual = [4, 4, 4, 7, 12, 14, 15, 14, 13, 12]
nonfiction_predicted = [4, 4, 4, 5, 6, 6, 7, 8, 9, 10]

ranges = [j + 3 for j in range(len(mae_past))]

for i in range(len(mae_past)):
    dif.append(abs(mae_past_genre[i] - mae_past[i]))
print(dif)

plt.subplot(2, 1, 1)
plt.ylim(1, 4.5)
plt.plot(ranges, mae_past, label='past')
plt.plot(ranges, mae_past_hybrid, label='past (hybrid)')
plt.plot(ranges, mae_past_quad, label='past (quad)')
plt.title("Fiction, k = 10")
plt.legend()

plt.subplot(2, 1, 2)
plt.ylim(1, 4.5)
plt.plot(ranges, mae_past_genre, label='past & genre')
plt.plot(ranges, mae_past_genre_hybrid, label='past & genre (hybrid)')
plt.plot(ranges, mae_past_genre_quad, label='past & genre (quad)')
plt.legend()

#plt.subplot(2, 1, 3)
#plt.plot(ranges, dif, label='difference')

plt.show()

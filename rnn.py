## RNN Model

#X = np.array(train_x.astype(float))

model = Sequential()
model.add(LSTM(64, input_shape=(train_x.shape[1:]),return_sequences=True))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(LSTM(64, return_sequences=True))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(LSTM(64))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(2, activation='sigmoid'))


opt = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)

# Compile model
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=opt,
    metrics=['accuracy']
)


## Train
#X = np.array(train_x.astype(float))
#validation_x = np.array(validation_x.astype(float))
RNN = model.fit(
    train_x, train_y,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(validation_x, validation_y)
    #callbacks=[tensorboard, checkpoint],
)

score = model.evaluate(validation_x, validation_y, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])

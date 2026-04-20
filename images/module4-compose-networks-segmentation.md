# 🎨 Иллюстрация: module4-compose-networks-segmentation

## Назначение
Показать сетевую сегментацию в Docker Compose: public-net и private-net.

## Схема
```
Internet
   ↓
[frontend] ──── public-net ──── [backend]
                                    │
                               private-net
                                    │
                                  [db]  ← недоступна из интернета!
```

### Блоки:
- Слева: иконка интернета → стрелка вниз
- Верхний слой (public-net, синий): frontend + backend
- Нижний слой (private-net, зелёный): backend + db
- Красный замок на db: "Только backend может достучаться"
- Надпись: "Сетевая сегментация — база защищена"

## Стиль
Два цветных горизонтальных слоя. Стрелки соединений. Иконки сервисов.

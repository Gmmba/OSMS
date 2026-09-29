
[y, Fs] = audioread('voice.wav');
disp(['Fs из файла: ', num2str(Fs), ' Гц']);

dur = 2.771;
Fs_calc = length(y) / dur;
disp(['Fs по формуле: ', num2str(Fs_calc), ' Гц']);

y1 = downsample(y, 10);
zvuk = audioplayer(y1, Fs/10);
play(zvuk);
figure; 
plot(y1);

N = length(y);
f = (0:N-1) * Fs / N;
A = abs(fft(y)) / N * 2;
N1 = length(y1);
f1 = (0:N1-1) * (Fs/10) / N1;
A1 = abs(fft(y1)) / N1 * 2;
h = 1:floor(N/2);
h1 = 1:floor(N1/2);

w  = f(find(A(h) > 0.05 * max(A(h)), 1, 'last'));
w1 = f1(find(A1(h1) > 0.05 * max(A1(h1)), 1, 'last'));
disp(['Ширина спектра оригинала: ', num2str(w), ' Гц']);
disp(['Ширина спектра прореженного: ', num2str(w1), ' Гц']);

figure;
subplot(2,1,1);
plot(f(h), A(h));
title('Спектр оригинала');
xlabel('Частота, Гц');
ylabel('Амплитуда');
subplot(2,1,2);
plot(f1(h1), A1(h1));
title('Спектр прореженного сигнала');
xlabel('Частота, Гц');
ylabel('Амплитуда');

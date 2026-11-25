x_b  = 14;
y_b  = 21;

x_bn = 15;
y_bn = 16;

gl   = zeros(1, 31);
gl_n = zeros(1, 31);

for i = 1:31

    fb_x = bitxor(bitget(x_b, 2), bitget(x_b, 1));
    fb_y = bitxor(bitget(y_b, 4), bitget(y_b, 1));

    gl(i) = bitxor(bitget(x_b, 1), bitget(y_b, 1));

    x_b = bitshift(x_b, -1) + fb_x * 16;
    y_b = bitshift(y_b, -1) + fb_y * 16;

    fb_x = bitxor(bitget(x_bn, 2), bitget(x_bn, 1));
    fb_y = bitxor(bitget(y_bn, 4), bitget(y_bn, 1));

    gl_n(i) = bitxor(bitget(x_bn, 1), bitget(y_bn, 1));

    x_bn = bitshift(x_bn, -1) + fb_x * 16;
    y_bn = bitshift(y_bn, -1) + fb_y * 16;

end


disp('Первая последовательность:');
disp(gl);

disp('Вторая последовательность:');
disp(gl_n);

gl_bip   = 2 * gl - 1;
gl_n_bip = 2 * gl_n - 1;

[acf_xcorr, lags_acf] = xcorr(gl_bip, 'coeff');
acf_auto = autocorr(gl_bip', 'NumLags', 30);

[ccf_xcorr, lags_ccf] = xcorr(gl_bip, gl_n_bip, 'coeff');

disp('Автокорреляция (xcorr):');
disp([lags_acf(lags_acf >= 0)', acf_xcorr(lags_acf >= 0)']);

disp('Автокорреляция (autocorr):');
disp([(0:30)', acf_auto(:)]);

disp('Взаимная корреляция (xcorr):');
disp([lags_ccf(lags_ccf >= 0)', ccf_xcorr(lags_ccf >= 0)']);

lags0 = 0:30;
r_x   = acf_xcorr(lags_acf >= 0);
r_a   = acf_auto(:)';

figure;

subplot(2,1,1);
stem(lags0, r_x, 'filled'); grid on;
title('Автокорреляция (xcorr)');
xlabel('Задержка (lag)');
ylabel('Коэффициент корреляции');
xticks(0:5:30);
ylim([-0.5 1.2]);

subplot(2,1,2);
stem(lags0, r_a, 'filled'); grid on;
title('Автокорреляция (autocorr)');
xlabel('Задержка (lag)');
ylabel('Коэффициент корреляции');
xticks(0:5:30);
ylim([-0.5 1.2]);
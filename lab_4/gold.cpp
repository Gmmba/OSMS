#include <iostream>
#include <iomanip>
using namespace std;

const int L = 15;

void mseq4(int xn, int out[]) {
    int x[4];
    for (int i = 0; i < 4; i++) x[i] = (xn >> (3 - i)) & 1;
    for (int t = 0; t < L; t++) {
        out[t] = x[3];
        int fx = x[2] ^ x[3];
        for (int i = 3; i > 0; i--) {
            x[i] = x[i - 1];
        }
        x[0] = fx;
    }
}

/*
void gold(int xn, int yn, int out[]) {
    int x[5], y[5];
    for (int i = 0; i < 5; i++) {
        x[i] = (xn >> (4 - i)) & 1;
        y[i] = (yn >> (4 - i)) & 1;
    }
    for (int t = 0; t < L; t++) {
        out[t] = x[4] ^ y[4];
        int fx = x[3] ^ x[4];
        int fy = y[3] ^ y[4];
        for (int i = 4; i > 0; i--) { x[i] = x[i-1]; y[i] = y[i-1]; }
        x[0] = fx;
        y[0] = fy;
    }
}
*/

double corr(const int a[], const int b[], int shift) {
    int matches = 0, mismatches = 0;
    for (int i = 0; i < L; i++) {
        if (a[i] == b[(i + shift) % L]) matches++;
        else mismatches++;
    }
    return (matches - mismatches) / (double)L;
}

void print_table(const int a[], const int b[], const char* name) {
    cout << "Сдвиг | " << L << " бит последовательности         | " << name << endl;
    cout << "------------------------------------------------------------" << endl;
    for (int s = 0; s <= L; s++) {
        cout << "  " << s << "   | ";
        for (int i = 0; i < L; i++) cout << b[(i + s) % L];
        cout << " | " << corr(a, b, s) << endl;
    }
}

void check_balance(const int a[]) {
    int ones = 0;
    for (int i = 0; i < L; i++) ones += a[i];
    int zeros = L - ones;
    int diff = ones > zeros ? ones - zeros : zeros - ones;
    cout << "1) Сбалансированность: единиц " << ones << ", нулей " << zeros;
    cout << (diff <= 1 ? " -> выполняется" : " -> НЕ выполняется") << endl;
}

void check_runs(const int a[]) {
    int cnt[L + 1] = {0};
    int total = 0, len = 1;
    for (int i = 1; i <= L; i++) {
        if (i < L && a[i] == a[i - 1]) len++;
        else {
            cnt[len]++; 
            total++; 
            len = 1; 
        }
    }
    cout << "2) Цикличность (свойство серий): всего серий " << total << endl;
    cout << fixed << setprecision(5);
    
    for (int k = 1; k <= L; k++) {
        if (cnt[k] > 0) {
            double actual_fraction = (double)cnt[k] / total;
            double ideal_fraction = 1.0 / (1 << k);
            
            cout << "   длина " << k << ": " << cnt[k] << " шт. ("
                 << "факт: " << actual_fraction 
                 << ", идеал: " << ideal_fraction << ")" << endl;
        }
    }
}



void check_corr(const int a[]) {
    double mx = -2, mn = 2;
    for (int s = 1; s < L; s++) {
        double c = corr(a, a, s);
        if (c > mx) mx = c;
        if (c < mn) mn = c;
    }
    cout << "3) Корреляция: пик при сдвиге 0 = " << corr(a, a, 0) << endl;
    cout << "   при сдвигах 1-" << L - 1 << ": min = " << mn << ", max = " << mx
         << " (идеал " << -1.0 / L << ")" << endl;
    cout << (mx < 0.5 ? "   пик острый, свойство выполняется" : "   НЕ выполняется") << endl;
}

int main() {
    int a[L];
    mseq4(0b1011, a);

    cout << "Последовательность: ";
    for (int i = 0; i < L; i++) cout << a[i];
    cout << "\n\n";

    check_balance(a);
    check_runs(a);
    check_corr(a);
    cout << endl;

    // print_table(a, a, "Автокорреляция");

    /*
    int b[L];
    mseq4(0b0110, b);
    cout << "Последовательность 2: ";
    for (int i = 0; i < L; i++) cout << b[i];
    cout << "\n\n";
    check_balance(b);
    check_runs(b);
    check_corr(b);
    print_table(a, b, "Взаим. корр.");
    */
    return 0;
}
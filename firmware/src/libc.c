/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Leo Kuroshita (@kurogedelic), Hügelton Instruments */
/* The few libc routines the compiler may call implicitly (struct copies,
 * zeroing). Freestanding: no other libc. */
void *memset(void *d, int c, unsigned n)
{
    unsigned char *p = d;
    while (n--)
        *p++ = (unsigned char)c;
    return d;
}

void *memcpy(void *d, const void *s, unsigned n)
{
    unsigned char *p = d;
    const unsigned char *q = s;
    while (n--)
        *p++ = *q++;
    return d;
}

int memcmp(const void *a, const void *b, unsigned n)
{
    const unsigned char *p = a, *q = b;
    for (; n; n--, p++, q++)
        if (*p != *q)
            return *p - *q;
    return 0;
}

static int str_eq(const char *a, const char *b)
{
    while (*a && *a == *b) {
        a++;
        b++;
    }
    return *a == *b;
}

static unsigned str_len(const char *s)
{
    unsigned n = 0;
    while (s[n])
        n++;
    return n;
}

static void str_cpy(char *d, const char *s, unsigned max)
{
    unsigned i = 0;
    while (s[i] && i + 1 < max) {
        d[i] = s[i];
        i++;
    }
    d[i] = 0;
}

/* decimal with an optional fixed point: fmt_fix(buf, -63, 1) -> "-6.3" */
static void fmt_fix(char *b, int32_t v, int decimals)
{
    char t[12];
    int n = 0, neg = v < 0, i;
    uint32_t u = (uint32_t)(neg ? -v : v);
    do {
        t[n++] = (char)('0' + u % 10u);
        u /= 10u;
        if (n == decimals)
            t[n++] = '.';
    } while (u || n <= decimals);
    if (neg)
        t[n++] = '-';
    for (i = 0; i < n; i++)
        b[i] = t[n - 1 - i];
    b[n] = 0;
}

static void fmt_int(char *b, int32_t v) { fmt_fix(b, v, 0); }

static uint32_t rng_state = 0x1234567u;
static uint32_t rng(void)
{
    rng_state ^= rng_state << 13;
    rng_state ^= rng_state >> 17;
    rng_state ^= rng_state << 5;
    return rng_state;
}

#if !defined(FELUCCA_WEB) && !defined(__APPLE__) && !defined(__linux__)
typedef __builtin_va_list va_list;
#define va_start(ap, param) __builtin_va_start(ap, param)
#define va_end(ap)          __builtin_va_end(ap)
#define va_arg(ap, type)    __builtin_va_arg(ap, type)

int snprintf(char *str, unsigned int size, const char *fmt, ...)
{
    if (!str || size == 0) return 0;
    va_list ap;
    va_start(ap, fmt);
    unsigned int out_idx = 0;
    const char *p = fmt;

    while (*p && out_idx + 1 < size) {
        if (*p != '%') {
            str[out_idx++] = *p++;
            continue;
        }
        p++;
        if (*p == '%') {
            str[out_idx++] = '%';
            p++;
            continue;
        }

        int is_long = 0;
        if (*p == 'l') {
            is_long = 1;
            p++;
        }

        if (*p == 'u' || *p == 'd' || *p == 'i') {
            char num_buf[16];
            uint32_t val;
            if (*p == 'u') {
                if (is_long) val = (uint32_t)va_arg(ap, unsigned long);
                else val = (uint32_t)va_arg(ap, unsigned int);
            } else {
                int32_t sval;
                if (is_long) sval = (int32_t)va_arg(ap, long);
                else sval = (int32_t)va_arg(ap, int);
                if (sval < 0) {
                    if (out_idx + 1 < size) str[out_idx++] = '-';
                    val = (uint32_t)(-sval);
                } else {
                    val = (uint32_t)sval;
                }
            }
            int ni = 0;
            do {
                num_buf[ni++] = (char)('0' + (val % 10u));
                val /= 10u;
            } while (val > 0 && ni < 15);
            while (ni > 0 && out_idx + 1 < size) {
                str[out_idx++] = num_buf[--ni];
            }
            p++;
        } else if (*p == 's') {
            const char *s = va_arg(ap, const char *);
            if (!s) s = "(null)";
            while (*s && out_idx + 1 < size) {
                str[out_idx++] = *s++;
            }
            p++;
        } else if (*p == 'c') {
            char c = (char)va_arg(ap, int);
            if (out_idx + 1 < size) str[out_idx++] = c;
            p++;
        } else {
            if (out_idx + 1 < size) str[out_idx++] = *p++;
        }
    }
    str[out_idx] = '\0';
    va_end(ap);
    return (int)out_idx;
}
#endif


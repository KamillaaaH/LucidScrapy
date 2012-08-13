/*
 * File:   support.c
 * Author: kamilla
 *
 * Created on August 12, 2012, 5:33 PM
 */

#include "hashset.h"
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <limits.h>
#include <assert.h>

/** Support functions */

struct frequency {
    char ch; // a particular letter
    int occurrences; // the number of times it occurs
};

static int HashFrequency(const void *elem, int numBuckets) {
    struct frequency *freq = (struct frequency *) elem;
    return (freq->ch % numBuckets);
}

static int CompareLetter(const void *elem1, const void *elem2) {
    struct frequency *freq1 = (struct frequency *) elem1;
    struct frequency *freq2 = (struct frequency *) elem2;
    return (freq1->ch - freq2->ch);
}

void CreateNewHashPy(int elemSize, int numBuckets) {
    hashset counts;
    vector sortedCounts;

    HashSetNew(&counts, elemSize, numBuckets, HashFrequency, CompareLetter, NULL);
}

void EnterItemPy(char item) {
    hashset counts;
    HashSetEnter(&counts, &item);
}

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
#include <string.h>
#include <time.h>
#include <regex.h>

/** Support functions */

hashset counts;
vector vec;

struct frequency {
    char s; // a particular string
    int occurrences; // the number of times it occurs
};

/*
 * Function: CompareLetter
 * ----------------------
 * Class of function designed to compare two elements, each identified
 * by address.  The HashSetCompareFunction compares these elements and
 * decides whether or not they are logically equal or or.
 */
static int CompareLetter(const void *elem1, const void *elem2) {
    struct frequency *freq1 = (struct frequency *) elem1;
    struct frequency *freq2 = (struct frequency *) elem2;
    return (freq1->s - freq2->s);
}

/**
 * Function: AddFrequency
 * ----------------------
 * Mapping function used to take a frequency stored
 * in a hashset and append it to an vector of frequencies.
 * The address of the vector is passed in as the auxiliarydata.
 */

static void AddFrequency(void *elem, void *v) {
    VectorAppend((vector *) v, elem);
}

/**
 * Function: PrintFrequency
 * -------------------------
 * Mapping function used to print one frequency stored in a hashset.  The
 * file is passed as the client data, so that it can be used to print to
 * any FILE *.
 */

static void PrintFrequency(void *elem, void *fp) {
    struct frequency *freq = (struct frequency *) elem;
    fprintf((FILE *) fp, "Data: %d\n",
            freq->s);
}

static void PrintString(void *elemAddr, void *auxData) {
    fprintf(stdout, "\n%s", (char*) elemAddr);
}

void Py_HashSetNew(int elemSize, int numBuckets) {
    HashSetNew(&counts, elemSize, numBuckets, CompareLetter, NULL);
}

void Py_HashSetEnter(const void *itemAddr, int position) {
    HashSetEnter(&counts, itemAddr, position);

}

void Py_PrintFn() {
    fprintf(stdout, "\nHere is the content of the table:\n");
    HashSetMap(&counts, PrintString, stdout); // print contents of table
}

void Py_HashSetDispose() {
    HashSetDispose(&counts);
}

void *regexp(char *string, char *patrn) {
    regex_t rgT;
    regmatch_t match;
    const char *p = string;
    if (regcomp(&rgT, patrn, REG_EXTENDED) != 0) {
        printf("\nCan't compile regex");
        exit(0);
    }
    
    while (regexec(&rgT, p, 1, &match, 0) == 0) {
        printf("\nSearching regex...");
        printf("\n%.*s", (int)(match.rm_eo - match.rm_so), &p[match.rm_so]);
        p += match.rm_eo; // or p = &p[match.rm_eo];
    }
}

void storeData() {
    time_t rawtime;
    struct tm *timeinfo;
    char buffer [80];

    time(&rawtime);
    timeinfo = localtime(&rawtime);

    strftime(buffer, 80, "%d%b%y_%H:%M.csv", timeinfo);
    puts(buffer);

    //FILE *fp;
    //fp = fopen(buffer, "w");
    char *data = "{\"DESPESA\":19283921, \"RECEITAS\":1298391, \"CODIGO\": 7}";
    /*if (!fp) {
        printf("\nCan't open the file!");
        exit(0);
    }*/
    char *match = regexp(data, "[[:alpha:]]+");
    //printf("\n->%s<-\n(b=%d e=%d)\n", match, b, e);
    //fputs(data, fp) != EOF;
    //fclose(fp); // or for the paranoid: if (fclose (fOut) == EOF) rc = 0;
}
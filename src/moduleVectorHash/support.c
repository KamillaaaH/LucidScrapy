/*
 * File:   support.c
 * Author: kamilla e maylon
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
#include "dirent.h"


/** Support functions */

hashset namesOfFiles;
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

void Py_HashSetNewNameOfFiles(int elemSize, int numBuckets) {
    printf("\nCreate new hashset");
    HashSetNew(&namesOfFiles, elemSize, numBuckets, CompareLetter, NULL);
}

void Py_HashSetEnterNameOfFiles(const void *itemAddr, int position) {
    //printf("\nModule C position = %d\n", position);
    HashSetEnter(&namesOfFiles, itemAddr, position);
}

void Py_PrintFn() {
    fprintf(stdout, "\nHere is the content of the table:\n");
    HashSetMap(&namesOfFiles, PrintString, stdout); // print contents of table
}

void Py_HashSetDispose() {
    HashSetDispose(&namesOfFiles);
}

/*FILE *getFilePointer(char *categoria) {
    time_t rawtime;
    struct tm *timeinfo;
    char buffer [80];
    char *filename;

    time(&rawtime);
    timeinfo = localtime(&rawtime);

    strftime(buffer, 80, "_%d%b%y_%H:%M.csv", timeinfo);

    filename = strcat(categoria, buffer);
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        printf("\nCan't open the file");
        exit(0);
    }
    return fp;
}*/

int putListFilesInHash() {
    DIR *dir;
    struct dirent *ent;
    dir = opendir("/home/kamilla/NetBeansProjects/LucidScrapy/src/dataDespesas");
    int i = 0;
    if (dir != NULL) {
        /* print all the files and directories within directory */
        while ((ent = readdir(dir)) != NULL) {
            printf("%s\n", ent->d_name);
            HashSetEnter(&namesOfFiles, ent->d_name, i);
            i++;
        }
        closedir(dir);
    } else {
        /* could not open directory */
        perror("");
        return EXIT_FAILURE;
    }

    return 0;
}

/*void splitFiles(){
    char *patrn = "[0-9]+";
    char *string;

    int CUR_MAX = 300;
    char *buffer = (char*) malloc(sizeof(char) * CUR_MAX); // allocate buffer.
    int count = 0;
    int length = 0;

    while ( (ch != '\n') && (ch != EOF) ) {
        if(count ==CUR_MAX) { // time to expand ?
          CUR_MAX *= 2; // expand to double the current size of anything similar.
          count = 0;
          buffer = realloc(buffer, CUR_MAX); // re allocate memory.
        }
        string = getc(file); // read from stream.
        buffer[length] = ch; // stuff in buffer.
        length++;
        count++;
    }

    free(buffer);
}*/

/*void *regexp(char *string, char *patrn) {
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
}*/

void storeData(FILE *fp) {
    /*printf("\nLet's store it 2 ");
    time_t rawtime;
    struct tm *timeinfo;
    char buffer [80];
    char *filename;

    time(&rawtime);
    timeinfo = localtime(&rawtime);

    strftime(buffer, 80, "_%d%b%y_%H:%M.csv", timeinfo);

    filename = strcat(categoria, buffer);
   
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        printf("\nCan't open the file");
        exit(0);
    }*/
    int i = 0;
    vector *vec = &namesOfFiles.v;
    for (i = 0; i < vec->logLength; i++) {
        char *data = (char *) vec->elems + (i * vec->elemSize);
        fprintf(fp, "\n%s", data);
    }

    fclose(fp);
}
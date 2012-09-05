/*
 * File:   support.h
 * Author: kamilla e maylon
 *
 * Created on August 12, 2012, 10:41 PM
 */

#ifndef _hashset_
#define _hashset_

void Py_HashSetNew(int elemSize, int numBuckets);
void Py_HashSetEnter(char item);
void Py_PrintFn();
void Py_HashSetDispose(hashset *h);
void storeData(FILE *fp);
static int CompareLetter(const void *elem1, const void *elem2);
static int HashFrequency(const void *elem, int numBuckets);
static void PrintString(void *elemAddr, void *auxData);
void SortItems();
FILE *getFilePointer(char *categoria);

#endif
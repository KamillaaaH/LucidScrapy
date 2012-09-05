/*
 * File:   vector.c
 * Author: kamilla e maylon
 *
 * Created on August 12, 2012, 5:32 PM
 */

#include "vector.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

void VectorNew(vector *v, int elemSize, VectorFreeFunction freeFn, int initialAllocation)
{
	assert(v != NULL);
	assert(elemSize > 0);
	assert(initialAllocation > -1);
	v->initialAllocation = initialAllocation;

	v->elems = 0;
	if(initialAllocation)
	{
		v->elems = malloc(initialAllocation*elemSize);
		assert(v->elems!=NULL);
		v->allocLength = initialAllocation;

	}
	else
	{
		printf("Setting default initialAllocation = 10\n");
		initialAllocation = 10;
		v->elems = malloc(initialAllocation*elemSize);
		assert(v->elems!=NULL);
		v->allocLength = initialAllocation;
	}

	v->elemSize = elemSize;
	v->logLength = 0;
	v->_free = freeFn;
}

void VectorDispose(vector *v)
{
	assert(v != NULL);
	// Apaga elemento por elemento
	printf("\nFreeing elements...");
	if(v->_free){
		int i;
		for(i = 0; i < v->logLength; i++)
			v->_free((char *)v->elems + (i * v->elemSize));
	}
	//Freeing vector
	if(v->elems)
		free(v->elems);
}

int VectorLength(const vector *v)
{
	assert(v != NULL);
	//return number of elements
	return v->logLength;
}

void *VectorNth(const vector *v, int position)
{
	/**An assert is raised if position is less than 0 or
	 * greater than the logical length minus 1
	 */
	assert(v != NULL);
	assert(position >= 0);
	if(v->logLength > 0)
		assert(position <= v->logLength -1);

	if(position > v->logLength - 1){
		printf("Out of range!\n");
		return NULL;
	}
	/**this function returns a pointer into
	 *the vector's storage
	 */
	return ((char*)v->elems + (position*v->elemSize));
}

void VectorReplace(vector *v, const void *elemAddr, int position)
{
	assert(v != NULL);
	assert(position >= 0);
	if(v->logLength > 0)
		assert(position <= v->logLength);

	if(position > v->logLength - 1){
		printf("Out of range!\n");
		return;
	}
	//freeing old elem
	if(v->_free)
		v->_free((char *)v->elems + (position * v->elemSize));

	//replacing
	assert(memcpy( ((char *)v->elems + (position * v->elemSize)), elemAddr, v->elemSize)!=NULL);
}

static void vectorGrow(vector *v)
{
	assert(v != NULL);
	v->allocLength*=2;
	v->elems = realloc(v->elems, v->allocLength * v->elemSize);
}


void VectorAppend(vector *v, const void *elemAddr)
{
	assert(v != NULL);
	//if the allocLength isn't enough
	if(v->logLength == v->allocLength)
		vectorGrow(v);

	assert(memcpy( (((char *)v->elems) + (v->logLength * v->elemSize)), elemAddr, v->elemSize)!=NULL);
	v->logLength++;
}


void VectorInsert(vector *v, const void *elemAddr, int position)
{
	assert(v != NULL);
	// An assert is raised if position is less than 0 or greater than the logical length.
	assert(position >= 0);
	if(v->logLength > 0)
		assert(position <= v->logLength);

	assert(position > -1);

	//if the allocLength isn't enough
	if(v->logLength == v->allocLength)
		vectorGrow(v);

	void *target = (char*)v->elems+(position*v->elemSize);
	void *end = (char*)v->elems+(v->logLength*v->elemSize);
	int total = ((char*)end - (char*)v->elems);


	//if position is 0
	if(target==v->elems)
	{
		char buffer[total];
		assert(memcpy(buffer, v->elems, total)!=NULL);
		assert(memcpy(v->elems, elemAddr, v->elemSize)!=NULL);
		assert(memcpy((char*)v->elems+v->elemSize, buffer, total)!=NULL);
		v->logLength++;
		return;
	}
	//if position is the last
	if(target==end)
	{
		VectorAppend(v, elemAddr);
		return;
	}
	//if position is on the middle
	int backSize = (char*)end - (char*)target;
	char buffer[backSize];
	assert(memcpy(buffer, target, backSize)!=NULL);
	assert(memcpy(target, elemAddr, v->elemSize)!=NULL);
	assert(memmove((char*)target+v->elemSize, buffer, backSize)!=NULL);
	v->logLength++;
}

/**Delete
 * Function: VectorDelete
 * ----------------------
 * Deletes the element at the specified position from the vector. Before the
 * element is removed,  the ArrayFreeFunction that was supplied to VectorNew
 * will be called on the element.
 *
 * An assert is raised if position is less than 0 or greater than the logical length
 * minus one.  All the elements after the specified position will be shifted over to fill
 * the gap.  This method runs in linear time.  It does not shrink the
 * allocated size of the vector when an element is deleted; the vector just
 * stays over-allocated.
 */

void VectorDelete(vector *v, int position)
{
	assert(v != NULL);
	/**An assert is raised if position is less than 0 or greater than the logical length
		*minus one.
		*/
	assert(position > -1);

	if(position > v->logLength - 1){
		printf("Out of range!\n");
		return;
	}

	void *target = (char*)v->elems + (position*v->elemSize);

	void *end = (char*)v->elems+(v->logLength*v->elemSize);

	int total = ((char*)end - (char*)v->elems);
	//printf("\ntarget = [%i], end = [%i], total = [%d]",target, end, total);

	// freeing old elem
	if(v->_free)
		v->_free((char *)v->elems + (position * v->elemSize));

	//if position is 0
	if((char*)target == (char*)v->elems)
	{
		assert(memcpy(target, (char*)v->elems+v->elemSize, total)!=NULL);
		v->logLength--;
		return;
	}else if((char*)target == (char*)end)
	{
		//if position is the last
		v->logLength--;
		return;
	}else {
		//if position is the last
		int backSize = (char*)end - (char*)target;
		assert(memmove(target, (char*)target + v->elemSize, backSize)!=NULL);
		v->logLength--;
	}
}

void VectorSort(vector *v, VectorCompareFunction compare)
{
	assert(v != NULL);
	//An assert is raised if the comparator is NULL
	assert(compare !=NULL);

	/**The  contents  of  the  array  are  sorted in ascending order
    *according to a comparison  function  pointed  to  by  compar,
    *which  is called with two arguments that point to the objects
    *being compared.
		**/
	qsort(v->elems, v->logLength, v->elemSize, compare);
}


void VectorMap(vector *v, VectorMapFunction mapFn, void *auxData)
{
	assert(v != NULL);
	//An assert is raised if the mapfn function is NULL.
	assert(mapFn !=NULL);
        int i = 0;
	for(i = 0; i < v->logLength; i++)
		mapFn(((char *)v->elems + (i * v->elemSize)), auxData);
}

static const int kNotFound = -1;
int VectorSearch(const vector *v, const void *key, VectorCompareFunction searchFn, int startIndex, bool isSorted)
{
	assert(v != NULL);
	/**An assert is raised if startIndex is less than 0 or greater than
		* the logical length. An assert is raised if the
		* comparator or the key is NULL*/
	assert(startIndex >= 0 && startIndex <= v->logLength);
	assert(searchFn !=NULL && key !=NULL);

	/**The isSorted parameter allows the client
	 * to specify that the vector is already in sorted order, in which case VectorSearch
	 * uses a faster binary search.  If isSorted is false, a simple linear search is
 	* used.  If a match is found, the position of the matching element is returned;
 	* else the function returns -1
	*/
	if(isSorted == true)
	{

		/**The  bsearch()  function  returns a pointer to a matching member of the
      *array, or NULL if no match is found.  If there  are  multiple  elements
      *that match the key, the element returned is unspecified.
			*/
		void *match =	bsearch(key, v->elems, v->logLength, v->elemSize, searchFn);
		if(match !=NULL)
			return ((char*)match - (char*)v->elems)/v->elemSize;
	}
	else
	{       int i = 0;
		for(i = 0; i<(v->logLength); i++)
		{
			void *elemAddr = (char*) v->elems + i*v->elemSize;
			if(searchFn(key, elemAddr) == 0)
				return (((char*)elemAddr - (char*)v->elems)/v->elemSize);
		}

	}
	return kNotFound;
} 

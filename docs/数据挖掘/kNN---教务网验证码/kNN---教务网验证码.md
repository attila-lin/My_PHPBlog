kNN---教务网验证码
======

还要简单介绍下kNN么？
就是说要test的东西，在k范围内，和哪一类最像，那他就算哪一类。

![kNN](220px-KnnClassification.svg.png 'kNN')

> Example of k-NN classification. The test sample (green circle) should be classified either to the first class of blue squares or to the second class of red triangles. If k = 3 (solid line circle) it is assigned to the second class because there are 2 triangles and only 1 square inside the inner circle. If k = 5 (dashed line circle) it is assigned to the first class (3 squares vs. 2 triangles inside the outer circle).               --来自wiki


	# -*- coding: utf-8 -*-
	import Image
	import urllib
	import urllib2

	from numpy import *
	import operator
	from os import listdir

	def classify0(inX, dataSet, labels, k):
		dataSetSize = dataSet.shape[0]
		diffMat = tile(inX, (dataSetSize,1)) - dataSet
		sqDiffMat = diffMat**2
		sqDistances = sqDiffMat.sum(axis=1)
		distances = sqDistances**0.5
		sortedDistIndicies = distances.argsort()     
		classCount={}          
		for i in range(k):
			voteIlabel = labels[sortedDistIndicies[i]]
			classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
		sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
		return sortedClassCount[0][0]

	def totwo(im):
		returnVect = zeros((1,187))
		x, y = im.size
		im = im.convert('RGBA')
		pixdata = im.load()
		for j in xrange(y):
			for i in xrange(x):
				if pixdata[i,j][0] < 150 and pixdata[i,j][1] < 150 and pixdata[i,j][2] > 0:
					# print '@',
					returnVect[0,11*i+j]=1
				else:
					# print '-',
					returnVect[0,11*i+j]=0
			# print ''
		return returnVect


	img = Image.open('CheckCode.aspx')
	# img.show()

	box0 = ( 4,3,14,19)#设置要拷贝的区域 
	box2 = (13,3,23,19)
	box4 = (22,3,32,19)
	box6 = (31,3,41,19)
	box8 = (40,3,51,19)



	img2 = Image.open('CheckCode(2).aspx')
	box3 = ( 4,3,14,19)#设置要拷贝的区域 
	box1 = (13,3,23,19)
	box5 = (31,3,41,19)
	box7 = (40,3,51,19)
	region0 = img.crop(box0)
	region2 = img.crop(box2)
	region4 = img.crop(box4)
	region6 = img.crop(box6)
	region8 = img.crop(box8)
	region3 = img2.crop(box3)
	region1 = img2.crop(box1)
	region5 = img2.crop(box5)
	region7 = img2.crop(box7)
	# print type(region0)
	trainingMat = zeros((9,187))
	trainingMat[0,:] = totwo(region0)
	trainingMat[1,:] = totwo(region1)
	trainingMat[2,:] = totwo(region2)
	trainingMat[3,:] = totwo(region3)
	trainingMat[4,:] = totwo(region4)
	trainingMat[5,:] = totwo(region5)
	trainingMat[6,:] = totwo(region6)
	trainingMat[7,:] = totwo(region7)
	trainingMat[8,:] = totwo(region8)
	# print trainingMat[0]

	hwLabels = ['0','1','2','3','4','5','6','7','8']


	pic_url = 'http://10.202.78.12/CheckCode.aspx'
	filename = 'heh'
	urllib.urlretrieve(pic_url,filename)


	che = Image.open(filename)
	# img.show()

	che0 = ( 4,3,14,19)#设置要拷贝的区域 
	che1 = (13,3,23,19)
	che2 = (22,3,32,19)
	che3 = (31,3,41,19)
	che4 = (40,3,51,19)
	cheion0 = che.crop(che0)
	cheion1 = che.crop(che1)
	cheion2 = che.crop(che2)
	cheion3 = che.crop(che3)
	cheion4 = che.crop(che4)
	# cheion4.show()
	vectorUnderTest0 = totwo(cheion0)
	vectorUnderTest1 = totwo(cheion1)
	vectorUnderTest2 = totwo(cheion2)
	vectorUnderTest3 = totwo(cheion3)
	vectorUnderTest4 = totwo(cheion4)

	classifierResult0 = classify0(vectorUnderTest0, trainingMat, hwLabels, 1)
	classifierResult1 = classify0(vectorUnderTest1, trainingMat, hwLabels, 1)
	classifierResult2 = classify0(vectorUnderTest2, trainingMat, hwLabels, 1)
	classifierResult3 = classify0(vectorUnderTest3, trainingMat, hwLabels, 1)
	classifierResult4 = classify0(vectorUnderTest4, trainingMat, hwLabels, 1)
	print classifierResult0
	print classifierResult1
	print classifierResult2
	print classifierResult3
	print classifierResult4

效果：


![result](Selection_176.png 'kNN')
def fitness(R):
    beta = 4.5e-6
    gamma = 0.01
    VTH = 0.69
    VDS = 5
    VGS = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    Vr = [1.00E-07, 2.50E-02, 1.00E-01, 2.25E-01, 4.00E-01, 6.25E-01, \
            9.00E-01, 1.23E+00, 1.57E+00, 1.84E+00, 2.07E+00]
    MSE = []
    f = 0
    for i in VGS:
        MSE.append(((beta/2)*((R[0])/R[1])*(i-VTH)**2)*(1+gamma*VDS)*25*((R[2]+1)*R[3]))
    for i in range(len(Vr)):
        f += (MSE[i]-Vr[i])**2
    f = (1/len(VGS))*f
    return -f
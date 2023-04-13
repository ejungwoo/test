#include "LKLogger.hpp"

void test_1D()
{
    const int    num_events = 10000;
    const int    num_particles = 10;
    double       x_array[10]; 
    
    const int    num_bins = 40;
    const double    bin_width = 0.2/num_bins;

    float        array_x_mean[80] = {0};
    float        array_x_renormalized[80] = {0};
    float        array_x_normalized[80] = {0};
    float        array_x_init[80] = {0};

    float        array_e[80] = {0};
    float        array_x_smeared[80] = {0};
    float        array_x_centeredP[80] = {0};
    float        array_x_centered2[80] = {0};
    float        his_convoluted_restore[80] = {0};
    float        array_x_something[80] = {0};
    

    double x_mean_squared_mean = 0.;
    double stddev_mean = 0.;

    const double x_max = 1.;
    const int    num_deconvolution = 2200;
    const double val_0p01 = 0.01;
    const int    seed=1234567;
    const double pi=4.*TMath::ATan(1.);
    

    auto hist_x_mean         = new TH1D("hist_x_mean",        "hist_x_mean",        2*num_bins,-x_max,x_max);//""[80] = {0};
    auto hist_x_mean_per_bin = new TH1D("hist_x_mean_per_bin","hist_x_mean_per_bin",2*num_bins,-x_max,x_max);//""[80] = {0};
    auto hist_x_renormalized = new TH1D("hist_x_renormalized","hist_x_renormalized",2*num_bins,-x_max,x_max);//""[80] = {0};
    auto hist_x_normalized   = new TH1D("hist_x_normalized",  "hist_x_normalized",  2*num_bins,-x_max,x_max);//""[80] = {0};
    auto hist_x_norm_per_bin = new TH1D("hist_x_norm_per_bin","hist_x_norm_per_bin",2*num_bins,-x_max,x_max);//""[80] = {0};
    auto hist_x_init         = new TH1D("hist_x_init",        "hist_x_init",        2*num_bins,-x_max,x_max);//""[80] = {0};
    hist_x_init -> SetMinimum(0);
    auto hist_x_smeared      = new TH1D("hist_x_smeared",     "hist_x_smeared",     2*num_bins,-x_max,x_max);//""[80] = {0};
    auto hist_e              = new TH1D("hist_e"        ,     "hist_e"        ,     2*num_bins,-x_max,x_max);//""[80] = {0};


    for (auto i_try=1; i_try<num_events; ++i_try) {
        double x_mean=0.;
        double x_squared_mean=0.;

        //lx_debug << i_try << endl;
        for (auto i_particle=1; i_particle<num_particles; ++i_particle)
        {
            double x_init = gRandom -> Uniform(-1,1);
            //lx_info << i_particle << " " << x_init << endl;
            x_array[i_particle] = x_init;
            x_mean          += x_init;
            x_squared_mean  += x_init*x_init;
        }

        x_mean              = x_mean         / num_particles;
        x_squared_mean      = x_squared_mean / num_particles;

        x_mean_squared_mean += x_mean*x_mean;

        double x_stddev = (x_squared_mean-x_mean*x_mean) / (num_particles-1);
        stddev_mean += x_stddev;

        int i_bin_x_mean = int(x_mean/bin_width);

        //lx_warning << i_bin_x_mean << " " << num_bins << " " << i_bin_x_mean+num_bins << endl;

        //array_x_mean[i_bin_x_mean+num_bins] = array_x_mean[i_bin_x_mean+num_bins] + 1.;
        hist_x_mean -> Fill(x_mean);
        hist_x_mean_per_bin -> Fill(x_mean);

        for (auto i_particle=1; i_particle<num_particles; ++i_particle)
        {
            double x_init = x_array[i_particle];
            //lx_info << x_init << endl;
            //int i_bin_x = int(x_init/bin_width);
            //array_x_init[i_bin_x+num_bins] = array_x_init[i_bin_x+num_bins]+1.;
            hist_x_init -> Fill(x_init);

            double x_normalized = (num_particles*x_mean - x_init) / (num_particles-1);
            double x_renormalized = x_init - x_normalized;

            //i_bin_x = int(x_renormalized/bin_width);
            //array_x_renormalized[i_bin_x+num_bins] = array_x_renormalized[i_bin_x+num_bins] + 1.;
            //int i_bin1 = int(x_normalized/bin_width);
            //array_x_normalized[i_bin1+num_bins] = array_x_normalized[i_bin1+num_bins] + 1.;
            hist_x_renormalized -> Fill(x_renormalized);
            hist_x_normalized -> Fill(x_normalized);
            hist_x_norm_per_bin -> Fill(x_normalized);
        }
    }





    x_mean_squared_mean = x_mean_squared_mean/num_events;

    double x_stddev = stddev_mean / num_events;
    double sigma2 = x_max/3./num_particles;

    std::cout << "x_mean_squared_mean" << " " << "x_stddev" << " " << "sigma2" << std::endl; // WRi_iterateE(*,*)
    std::cout << x_mean_squared_mean << " " << x_stddev << " " << sigma2 << std::endl; // WRi_iterateE(*,*)
    
    //array_x_mean=array_x_mean/(bin_width*num_events);
    //array_x_normalized=array_x_normalized/(bin_width*num_events*num_particles);
    hist_x_mean_per_bin -> Scale(1./bin_width*num_events);
    hist_x_norm_per_bin -> Scale(1./bin_width*num_events);


    double SIG=TMath::Sqrt(sigma2);
    double norm_factor=1./(SIG*TMath::Sqrt(pi+pi));


    for (auto i_bin=-num_bins; i_bin<num_bins; ++i_bin) {
        double X=i_bin*bin_width;
        double xx=TMath::Exp(-.5*X*X/sigma2)*norm_factor;
        //std::cout << setw(10) << X << setw(10) << xx << setw(10) << hist_x_mean -> GetBinContent(i_bin+num_bins) << std::endl; // WRi_iterateE(*,*)
    }
    std::cout << " " << std::endl; // WRi_iterateE(*,*)
    
    /// renormalized width of average position: ptcle vs rest
    double sig2_norm=x_stddev*num_particles/(num_particles-1);
    double sig_norm=TMath::Sqrt(sig2_norm);
    double norm_factor_norm=1./(sig_norm*TMath::Sqrt(pi+pi));
    double pfot=0.;

    for (auto i_bin=-num_bins; i_bin<num_bins; ++i_bin) {
        double X=i_bin*bin_width;
        /// estimated smearing function
        //array_x_smeared[i_bin+num_bins]=norm_factor_norm*TMath::Exp(-.5D0*X*X/sig2_norm)*bin_width;
        //std::cout << X << " " << array_x_smeared[i_bin+num_bins]/bin_width << " " << array_x_normalized[i_bin+num_bins] << std::endl; // WRi_iterateE(*,*)
        //pfot = pfot + array_x_smeared[i_bin+num_bins];

        double x_smeared = norm_factor_norm*TMath::Exp(-.5*X*X/sig2_norm)*bin_width;
        std::cout << X << " " << x_smeared << " " << hist_x_normalized -> GetBinContent(i_bin+num_bins) << std::endl; // WRi_iterateE(*,*)
        hist_x_smeared -> SetBinContent(i_bin+num_bins,x_smeared);
        pfot = pfot + x_smeared;
    }
    std::cout << "PTO=" << " " << pfot << std::endl; // WRi_iterateE(*,*)
    std::cout << " " << std::endl; // WRi_iterateE(*,*)
    
    for (auto i_bin=-num_bins; i_bin<num_bins; ++i_bin) {
        //array_e[i_bin+num_bins]=TMath::Sqrt(MAX(array_x_renormalized[i_bin+num_bins],1.));
        double x_e = TMath::Sqrt(MAX(array_x_renormalized[i_bin+num_bins],1.));
        /hist_e -> 
    }
    
    /*
    ///(*) array_x_init=array_x_init/(bin_width*num_events*num_particles)
    ///(*) array_x_renormalized=array_x_renormalized/(bin_width*num_events*num_particles)
    array_x_init=array_x_init/(bin_width*num_events);
    array_x_renormalized=array_x_renormalized/(bin_width*num_events);
    
    for (auto i_bin=-num_bins; i_bin<num_bins; ++i_bin) {
        A=0.;
        for (auto j_bin=-num_bins; j_bin<num_bins; ++j_bin) {
            i_bin2=i_bin-j_bin;
            if (TMath::Abs(i_bin2)<=num_bins) {
                A=A+array_x_smeared[j_bin+num_bins]*array_x_init[i_bin2+num_bins];
            }
        }
        /// smeared theoretically
        array_x_centeredP[i_bin+num_bins]=A;
    }


    
    array_x_centered2=array_x_renormalized;
    DTO=0.;
    for (auto i_bin=-num_bins; i_bin<num_bins; ++i_bin) {
        DTO=DTO+array_x_renormalized[i_bin+num_bins];
    }
    /// deconvolution
    for (auto i_iterate=1; i_iterate<num_deconvolution; ++i_iterate) {
        for (auto i_bin=-num_bins; i_bin<num_bins; ++i_bin) {
            A=0.;
            for (auto j_bin=-num_bins; j_bin<num_bins; ++j_bin) {
                i_bin2=i_bin-j_bin;
                if (TMath::Abs(i_bin2)<=num_bins) {
                    A=A+array_x_smeared[j_bin+num_bins]*array_x_centered2[i_bin2+num_bins];
                }
            }
            /// convoluted current restore w/blurring function
            his_convoluted_restore[i_bin+num_bins]=A;
            ///(*) write(*,*)'ia,c ',ia,a
        }
        for (auto i_bin2=-num_bins; i_bin2<num_bins; ++i_bin2) {
            A=0.;
            for (auto j_bin=-num_bins; j_bin<num_bins; ++j_bin) {
                i_bin=i_bin2+j_bin;
                if (TMath::Abs(i_bin)<=num_bins) {
                    if (his_convoluted_restore[i_bin+num_bins]>0.) {
                        A=A+array_x_smeared[j_bin+num_bins]*array_x_renormalized[i_bin+num_bins]/his_convoluted_restore[i_bin+num_bins];
                        ELSE;
                        A=A+array_x_smeared[j_bin+num_bins];
                    }
                }
            }
            FA=1.;
            if (TMath::Abs(i_bin2)<num_bins) {
                if (array_x_centered2[i_bin2+num_bins]>array_x_centered2[i_bin2-1+num_bins]&&array_x_centered2[i_bin2+num_bins]>array_x_centered2[i_bin2+1+num_bins]) {
                    ///(!) Added to previous line
                    FA=1./(1.+val_0p01);
                }
                else if (array_x_centered2[i_bin2+num_bins]<array_x_centered2[i_bin2-1+num_bins]&&array_x_centered2[i_bin2+num_bins]<array_x_centered2[i_bin2+1+num_bins]) {
                    ///(!) Added to previous line
                    FA=1./(1.-val_0p01);
                }
            }
            array_x_something[i_bin2+num_bins]=array_x_centered2[i_bin2+num_bins]*FA*A**1.99D0;
            ///(*) write(*,*)'ia,a,fa ',ias,a,fa
        }
        DVTO=0.;
        for (auto i_bin=-num_bins; i_bin<num_bins; ++i_bin) {
            DVTO=DVTO+array_x_something[i_bin+num_bins];
        }
        /// restored
        array_x_centered2=array_x_something*DTO/DVTO;
    }
    
    std::cout << "XVA" << " " << "MES" << " " << "SME" << " " << "TRU" << " " << "RES" << std::endl; // WRi_iterateE(*,"(5(2X,A,3X))")
    for (auto i_bin=-num_bins; i_bin<num_bins; ++i_bin) {
        X=i_bin*bin_width;
        std::cout << X << " " << array_x_renormalized[i_bin+num_bins] << " " << array_x_centeredP[i_bin+num_bins] << " " << array_x_init[i_bin+num_bins] << " " << array_x_centered2[i_bin+num_bins] << std::endl; // WRi_iterateE(*,"(1X,F5.2,4(1X,F7.4))")
        ///(!) Added to previous line
    }
    std::cout << " " << std::endl; // WRi_iterateE(*,*)
    
    }
    */

    //new TCanvas(); hist_x_mean -> Draw();
    //new TCanvas(); hist_x_init -> Draw();
    //new TCanvas(); hist_x_renormalized -> Draw();
    //new TCanvas(); hist_x_normalized -> Draw();
    //new TCanvas(); hist_x_mean_per_bin -> Draw();
    //new TCanvas(); hist_x_norm_per_bin -> Draw();
    new TCanvas(); hist_x_smeared -> Draw();
}

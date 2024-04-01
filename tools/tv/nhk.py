# coding:utf-8
import util

nhk_areas = ["130","010","011","012","013","014","015","016","020","030","040","050","060","070","080","090","100","110","120","140","150","160","170","180","190","200","210","220","230","240","250","260","270","280","290","300","310","320","330","340","350","360","370","380","390","400","401","410","420","430","440","450","460","470"]

IMG_COMMENT = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAArtJREFUeNrcWctxwjAQFUwaoAUoAUqAEmgBSoAS4MYVLnCGEqAEKAFKgBIcvQxPs14kWUri4MnOaLAlW3r79icZUxSFsbKyrWhYWz2xNRKcA2lkx3a7Ld4twKBANgecD2TLoXzauynSarW+ftupL9xuN7NcLs3lcvlboKkMjkYjczqdzHA4NMfjMaoIWop0Oh3T7/ejDH6kTARgaJBut+uueY9G6fV6WQwB4Pl8/hmDg8EgatrFYmFms9nX9XQ6LTFIZQAEjFEej4ebExaBZXwMuigOiV3cRZSdxDW7YKnfJ3Zh98z1en0Z5xieC41FAVrq3YOWodLY/X4PjmnlrAt4x38EEACsSdwCuA8x62MHgvdCCkjl9dwSoDdI4B+IWvxC4F/SB9GPlAOB78Dn4F/Sx+bzufPFyWTysgbn0+/55IVB6TupDWyDFQgY0+YHS2CdjdYJ+W+liTkRx2EuGRxYgAHDxcbjcQkcnqXs93uvYuv1+nsANZO6T2rOxdFHpQBW+hau0UelcB0CV+mDuSJ9CP7KnAg/RRK3YFzV4H2qfNRVQxEECBQWASRs3ANoLQAZtYxMbh5kny6PjHKdIXIkGSDZkJsC3SflcDiUlJNKUDEK0lAs1SQFCa7RGASIUN3HwEHizklRsUqSzKA2FTTWfZohBAX9DQxuNhu3udA7mqxEnZtmZJ9kTzLjmysmv5pmdBCQ3RDDtQSJ3J8xSnUfzWVZrKyvb8uDMv+F0gs2Itq/mdyzfBClSNfUmK/KUpe70fiWD1LrHHP5tla1RTEKOsbsoskMVj2TG8XtqtMcT27vknasVNHEVemizsN80AfpL2BP+wj8CUdRXfh/K7UkMSjPI74xH7hQgNTy6YMH65B59SeOlKrB/WAs5+nC8H++br09ine7XWNAaSyN/wTc7I/oTf8b4lOAAQCgsVv038qR/wAAAABJRU5ErkJggg=="

IMG_STEREO = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAiRJREFUeNrsmctxwjAQhuVMGqAFWqAFt4BLMCXQAty4wgXOUIIpAUqAEqAEoV9BzCKEtXpMomSyMxoTgvGnf7UPCSGlFMoWasjCxuLOViTcA1LQN9brtfxpA4MFWQ6cC7J6UN79XYpVVaWvH6JwKx7wM/bG3W4nzuez2O/3+m9zhQ0GAzEajcRwONRjPB7ra6zJryXot8vlImezmVQAwSmjrmvZdR07UIKD5Hg8islkoq/UjEoK4Ol9KAqFMaipCYrpdMoOEpaCUE5BPCmiHiJPp5NXCaim3P10L7zAVZAFiC+kD1gul0F5DRO0IX2TCwKk6uFBMQYlKWDbtixAVpqh6wgRGmNYozSS7bWZFMU0avEaLoux7Xar78fwLZMgF8Md1D1wMydAUiwIEDCu3KcSsFYiVtFsgLDD4fASibaqSD1wYw7gYEBjUKwPNBdwNCB1O/Ij3MwpffgcYL8N0LUEDLBddejA/zg1OTtgn8Iu0KxpJgesnap85Y4NaFosDLgxxeyajiBKBqQzRzCkGCZr94jJtZjWz+v1+tIPhlhMHfcConWnNp/PowFXq9VLA5GlWYArQhtOV7sV0nQk12JAcxIvAssVwdw0E7QnaZrG2ceZXs+sV7NWMfDaXocKTu/0su1J7JTTVyneDXgAaYVbl5OPPqAOdm5GJbqDM/tiuj/2KfZOwf+zmT9/NvN7ADebTTFQNkvxR8BlH6KX/jPETYABABrtSu0F1sjRAAAAAElFTkSuQmCC"

IMG_SS = "data:image/svg+xml,%3csvg%20width='20'%20height='20'%20viewBox='0%200%2020%2020'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M16.4%202.8C16.841%202.8%2017.2%203.159%2017.2%203.6V16.4C17.2%2016.841%2016.841%2017.2%2016.4%2017.2H3.6C3.159%2017.2%202.8%2016.841%202.8%2016.4V3.6C2.8%203.159%203.159%202.8%203.6%202.8H16.4ZM16.4%202H3.6C2.716%202%202%202.716%202%203.6V16.4C2%2017.284%202.716%2018%203.6%2018H16.4C17.284%2018%2018%2017.284%2018%2016.4V3.6C18%202.716%2017.284%202%2016.4%202Z'%20fill='black'/%3e%3cpath%20d='M5.16725%206.55501C5.24325%205.65901%205.81525%205.58301%206.30125%205.58301H9.28125C9.70225%205.58301%209.75625%205.90701%209.75625%206.02601C9.75625%206.09101%209.74525%206.48001%209.28125%206.48001H6.58225C6.34525%206.48001%206.07525%206.52301%206.04225%206.94401L5.84825%209.13601C6.15025%208.88801%206.55025%208.56401%207.46825%208.56401C8.62325%208.56401%2010.1892%209.38501%2010.1892%2011.501C10.1892%2013.423%208.81825%2014.405%207.30625%2014.405C5.37325%2014.405%204.53125%2012.861%204.53125%2012.203C4.53125%2011.771%204.92025%2011.739%205.01725%2011.739C5.40625%2011.739%205.47125%2011.944%205.61125%2012.365C5.81625%2012.981%206.43225%2013.51%207.29525%2013.51C8.21325%2013.51%209.14125%2012.895%209.14125%2011.48C9.14125%209.97901%208.07225%209.46101%207.28425%209.46101C7.05725%209.46101%206.43125%209.50401%205.98825%209.95801C5.61025%2010.347%205.56725%2010.39%205.32925%2010.39C4.82225%2010.39%204.86525%209.96901%204.87525%209.81801L5.16725%206.55701V6.55501Z'%20fill='black'/%3e%3cpath%20d='M12.2089%2013.724C12.2089%2014.102%2011.8959%2014.404%2011.5179%2014.404C11.1399%2014.404%2010.8379%2014.102%2010.8379%2013.724C10.8379%2013.335%2011.1399%2013.033%2011.5179%2013.033C11.8959%2013.033%2012.2089%2013.335%2012.2089%2013.724Z'%20fill='black'/%3e%3cpath%20d='M12.3602%207.94698C12.2312%207.94698%2011.9932%207.84998%2011.9932%207.55798C11.9932%207.23398%2012.1122%207.21298%2012.8142%207.08298C13.6892%206.93198%2014.0342%206.41298%2014.2182%205.78698C14.2722%205.60298%2014.3482%205.35498%2014.6822%205.35498C14.9302%205.35498%2015.1252%205.52798%2015.1252%205.74398V13.896C15.1252%2014.307%2014.8232%2014.403%2014.6072%2014.403C14.2612%2014.403%2014.0782%2014.209%2014.0782%2013.896V7.94698H12.3612H12.3602Z'%20fill='black'/%3e%3c/svg%3e"

IMG_BILINGUAL = "data:image/svg+xml,%3csvg%20width='20'%20height='20'%20viewBox='0%200%2020%2020'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M16.4%202.8C16.841%202.8%2017.2%203.159%2017.2%203.6V16.4C17.2%2016.841%2016.841%2017.2%2016.4%2017.2H3.6C3.159%2017.2%202.8%2016.841%202.8%2016.4V3.6C2.8%203.159%203.159%202.8%203.6%202.8H16.4ZM16.4%202H3.6C2.716%202%202%202.716%202%203.6V16.4C2%2017.284%202.716%2018%203.6%2018H16.4C17.284%2018%2018%2017.284%2018%2016.4V3.6C18%202.716%2017.284%202%2016.4%202Z'%20fill='black'/%3e%3cpath%20d='M14.9546%2013.496C15.0986%2013.496%2015.4946%2013.496%2015.4946%2014.012C15.4946%2014.516%2015.1226%2014.528%2014.9546%2014.528H4.97164C4.81564%2014.528%204.43164%2014.528%204.43164%2014.012C4.43164%2013.496%204.80364%2013.496%204.97164%2013.496H14.9556H14.9546ZM14.1746%206.08002C14.3426%206.08002%2014.7146%206.08002%2014.7146%206.58402C14.7146%207.05202%2014.4146%207.10002%2014.1746%207.10002H5.73964C5.60764%207.10002%205.21164%207.10002%205.21164%206.60902C5.21164%206.16402%205.43964%206.08102%205.73964%206.08102H14.1756L14.1746%206.08002Z'%20fill='black'/%3e%3c/svg%3e"

IMG_MULTISOUND = "data:image/svg+xml,%3csvg%20width='20'%20height='20'%20viewBox='0%200%2020%2020'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M16.4%202.8C16.841%202.8%2017.2%203.159%2017.2%203.6V16.4C17.2%2016.841%2016.841%2017.2%2016.4%2017.2H3.6C3.159%2017.2%202.8%2016.841%202.8%2016.4V3.6C2.8%203.159%203.159%202.8%203.6%202.8H16.4ZM16.4%202H3.6C2.716%202%202%202.716%202%203.6V16.4C2%2017.284%202.716%2018%203.6%2018H16.4C17.284%2018%2018%2017.284%2018%2016.4V3.6C18%202.716%2017.284%202%2016.4%202Z'%20fill='black'/%3e%3cpath%20d='M12.412%204.92202C12.82%204.92202%2013.408%204.93502%2013.408%205.59502C13.408%206.30302%2012.4%207.17902%2011.644%207.76702C10.336%208.77502%208.87201%209.56702%207.30001%2010.058C6.25601%2010.382%205.34401%2010.503%205.18801%2010.503C4.76801%2010.503%204.70801%2010.107%204.70801%209.98702C4.70801%209.60302%205.00801%209.57902%205.18801%209.55502C6.40001%209.43502%207.61201%209.08702%208.71601%208.54702C8.24801%207.92302%207.66001%207.29902%207.09601%206.80702C6.62801%207.08302%205.70401%207.55102%205.36801%207.55102C5.09201%207.55102%204.92401%207.25102%204.92401%207.03502C4.92401%206.79502%205.09201%206.72302%205.26001%206.65102C6.97601%205.99102%207.94801%205.15102%208.27201%204.82802C8.92001%204.18002%209.01601%204.07202%209.28001%204.07202C9.47201%204.07202%209.80801%204.16802%209.80801%204.44402C9.80801%204.61202%209.71201%204.70802%209.50801%204.92402H12.412V4.92202ZM14.212%209.23002C14.644%209.23002%2015.28%209.23002%2015.28%209.99802C15.28%2010.922%2013.648%2013.107%2010.396%2014.33C8.18801%2015.158%206.16001%2015.218%206.07601%2015.218C5.53601%2015.218%205.53601%2014.738%205.53601%2014.666C5.53601%2014.246%205.84801%2014.222%206.14801%2014.198C7.64801%2014.102%209.11201%2013.766%2010.504%2013.226C10.096%2012.566%209.52001%2011.834%209.00401%2011.294C7.86401%2011.882%206.78401%2012.254%206.46001%2012.254C6.12401%2012.254%206.00401%2011.942%206.00401%2011.738C6.00401%2011.414%206.23201%2011.342%206.44801%2011.282C7.82801%2010.922%209.70001%2010.07%2011.068%208.75002C11.176%208.65402%2011.608%208.19802%2011.716%208.11402C11.8%208.03002%2011.92%208.00602%2012.016%208.00602C12.292%208.00602%2012.544%208.21002%2012.544%208.41402C12.544%208.54602%2012.448%208.66602%2012.4%208.72602C12.256%208.89402%2012.004%209.14602%2011.92%209.23002H14.212ZM8.58401%205.78602C8.36801%205.95402%208.18801%206.09802%207.85201%206.33802C8.44001%206.80602%209.23201%207.65802%209.59201%208.07802C11.296%207.08202%2012.1%206.14602%2012.1%205.96602C12.1%205.78602%2011.956%205.78602%2011.752%205.78602H8.58401ZM10.912%2010.082C10.36%2010.502%2010.048%2010.694%209.84401%2010.826C10.492%2011.498%2011.236%2012.494%2011.452%2012.782C12.88%2012.038%2014.116%2010.778%2014.116%2010.286C14.116%2010.082%2013.984%2010.082%2013.672%2010.082H10.912Z'%20fill='black'/%3e%3c/svg%3e"

IMG_SUB = "data:image/svg+xml,%3csvg%20width='20'%20height='20'%20viewBox='0%200%2020%2020'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M16.4%202.8C16.841%202.8%2017.2%203.159%2017.2%203.6V16.4C17.2%2016.841%2016.841%2017.2%2016.4%2017.2H3.6C3.159%2017.2%202.8%2016.841%202.8%2016.4V3.6C2.8%203.159%203.159%202.8%203.6%202.8H16.4ZM16.4%202H3.6C2.716%202%202%202.716%202%203.6V16.4C2%2017.284%202.716%2018%203.6%2018H16.4C17.284%2018%2018%2017.284%2018%2016.4V3.6C18%202.716%2017.284%202%2016.4%202Z'%20fill='black'/%3e%3cpath%20d='M10.4922%2014.092C10.4922%2014.512%2010.4562%2015.112%209.8082%2015.304C9.5682%2015.376%208.6802%2015.376%208.3202%2015.376C7.6122%2015.376%207.2762%2015.376%207.2762%2014.836C7.2762%2014.344%207.6602%2014.344%207.7802%2014.344C7.8042%2014.344%208.7882%2014.368%208.8482%2014.368C9.1122%2014.368%209.4722%2014.368%209.4722%2013.828V11.632H4.9002C4.7682%2011.632%204.4082%2011.632%204.4082%2011.176C4.4082%2010.756%204.6962%2010.708%204.9002%2010.708H9.4722V9.77199C9.4722%209.66399%209.4722%209.31699%209.9282%209.31699C10.0722%209.31699%2010.2042%209.36499%2010.2882%209.38899C10.8402%209.13699%2011.1762%208.95699%2011.2962%208.89699C11.7282%208.66899%2011.7882%208.62099%2011.7882%208.53699C11.7882%208.40499%2011.6802%208.40499%2011.5362%208.40499H6.8442C6.7122%208.40499%206.3522%208.40499%206.3522%207.96099C6.3522%207.52899%206.6762%207.51699%206.8442%207.51699H12.0762C12.5202%207.51699%2013.1322%207.51699%2013.1322%208.22499C13.1322%208.71699%2012.8202%208.95699%2012.0882%209.36499C11.5842%209.64099%2010.8162%2010.013%2010.4922%2010.157V10.709H15.0882C15.2202%2010.709%2015.5802%2010.721%2015.5802%2011.177C15.5802%2011.609%2015.2802%2011.633%2015.0882%2011.633H10.4922V14.093V14.092ZM13.9842%205.29599C14.8842%205.29599%2015.2562%205.59599%2015.2562%206.56799V7.89999C15.2562%208.07999%2015.2442%208.40399%2014.7522%208.40399C14.2722%208.40399%2014.2362%208.11599%2014.2362%207.89999V6.71199C14.2362%206.32799%2014.0442%206.17099%2013.6962%206.17099H6.2682C5.9322%206.17099%205.7282%206.32699%205.7282%206.71199V7.89999C5.7282%208.09199%205.7162%208.40399%205.2362%208.40399C4.7562%208.40399%204.7322%208.12799%204.7322%207.89999V6.56799C4.7322%205.60899%205.0922%205.29599%206.0042%205.29599H9.4602V4.68399C9.4602%204.52799%209.4842%204.23999%209.9522%204.23999C10.3002%204.23999%2010.5042%204.33499%2010.5042%204.68399V5.29599H13.9842Z'%20fill='black'/%3e%3c/svg%3e"

IMG_SIGN = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAWNJREFUeNrsWcENgzAMNFUXYAVWYAUYgRVgBFbg2TcfeLMCrMAKjAAjpHHaVG1EoIRArSonWZEiiE92cjgGGGPAcePGiNntyY0kuRdJeJ+oqor9GshBIUmH3BxJ78XymW8q8DxPjBcgjusZTvq+h2maxDgMgxjRoiiCtm2XI7mW4q7rZufRETpV59DW3pXwfR/GcVxM8WIEsyyDsiytRTIIgg9LkmRfinERHTA9umjje2maQhiGH8RMwR4Z3g+5FidvbS3yp9gRtAHtHmya5vCCgB8k8z34rmlHYc2HsVDPIY5jMaK8FEWxSRt1Qu1kxskMWZnB43/W3YNXNULSNu3BMyRGAss2nT+tzKi13VEyI+tCWfk4mXEy4wj+G8GriWapNz2UiS1Vz6GXpjzPV78M+MzPZAajtQS8jnKC9no0Js0j2cr45q68t3nkulvWZKauazKkVC7kW8C0m+jUf0PcBRgAAxRlO2wJrDYAAAAASUVORK5CYII="

IMG_DATA = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAb5JREFUeNrsWdGRgjAUDDfXAJRAC7YgJUgJUIIt4J+/fOk3lCAlQAlYApSQy+YMExEEjwDvZtiZDAko7LyXbPYB45wzgbNonFg7P7iRJNeQZPqJy+XC1wY4tEjSIddF0mpYPvJNBZZlyeMXI45FCd7vd+Z5HsuyTI5932eO48jz78B/Mzw/kiSRz7JtW473+70cB0Hw8tvV5iAiVtc1E2SbKAJVVTFB/GUODkZQ/JG7rmtE16IoktFCH9EDEE2M4zjujOAgwTzPjQnvbrfjZVk2fZV29PGcP6c4DENWFMXk9B6PR3Y4HOSiQDr1lPbJzKaD/0oHN4Jr4LvvAsQUIorjnFAr++OtDsK5hCnFJtAFdb03xULp3+qUKQxFz6gOPu2fE+9nXAd1y2Qy8rMQFPOKHkF9ryZJULlkQLgTowtpsqOGZ9SlA5ZqKkb7wTFQJlT3eWQI3m63p+hhTIagKoJUE6JrrMCaRBD2XFVkemoxF1cjiNSh6AGRrlrDJLmPCarKq6sJNzJLDT2aYFtCVMPKNSEnQwRHmYXT6cTSNJUCDJezhNPZqjrje/H1eiVDqs2F/Ctg2i/RqX+G+BFgAB1oOJ1sLZI+AAAAAElFTkSuQmCC"

IMG_INTER = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAn9JREFUeNrsmcmRwjAQReUpEoAQSIEUIARSgBAgBLhxhQucSQFCgBAgBAjB4++hXR9Na/FCjQ7TVS7AlqWnXr5kY/I8N4VtiiNP7Ni82JKEqyANn9jv9/lfGxgsyHTgNMisonzFOxXLsqz8/DKJW8938Xq9mufzGexkPB6//T6fz8F7+v2+GY1GUZD5T4Tf7XK5RFdbMVjZHrZaraLvKwDzx+Oh5uGvIrHtdruVA9cZDHY8HmtJyWw2awYYY5j9dDrN6/ZxOp2qe4r08AK2KpI6eeTLWZ91VsWAFdvtdma9XjvbcuGFJthrCyYVywPN5/PqnOYtqIM2sUYeXC6XZjAYlF6pawzCdr/foz34FTMIQgKvANblQfbUcDj09smAobbBKkalQkI0WYAUyfntdludR2X6KlSuF3DOcWvJjAuSNQ/SISZiDR3V+gppIAP2Yiu0ADCTyaQMueQjJ7gWYqQGwslh5GWw1VIX40mX2LKXOPQweE2uuZa5ViuJBomQ2iZtsNLwvbJ8+sLbeqnDQEhwl5fsTYN4Cu20nP3IWsyAvJvxVbjc46veTgDZE76tk4QZQOxRzeOdArL3FouFUzZcE4mxxoDsCQHiorFDzZPRrncKiM6lCvEpIeXNrQ3A+8VY7zUCtOXFlhZA4uD2rHl18q8RIA8W8oQ9GXznx4fOi4ThMBB7SqtwhpHqtgsmBBkFqIXJleQQXtmluKTHfuJD342f6rQlTZu1BuZa/jTpQZVrkw4C8mwRMmyttEdTbeMQkhINsjagSIprhrbOwduh9dXuXyIEsf/Ic7GkQqz4ukB9Ofj/dqutVYCHwyEZKJsl+VfAab9ET/1viG8BBgCSNPvEZxdw6AAAAABJRU5ErkJggg=="

IMG_RE = "data:image/svg+xml,%3csvg%20width='20'%20height='20'%20viewBox='0%200%2020%2020'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M16.4%202.8C16.841%202.8%2017.2%203.159%2017.2%203.6V16.4C17.2%2016.841%2016.841%2017.2%2016.4%2017.2H3.6C3.159%2017.2%202.8%2016.841%202.8%2016.4V3.6C2.8%203.159%203.159%202.8%203.6%202.8H16.4ZM16.4%202H3.6C2.716%202%202%202.716%202%203.6V16.4C2%2017.284%202.716%2018%203.6%2018H16.4C17.284%2018%2018%2017.284%2018%2016.4V3.6C18%202.716%2017.284%202%2016.4%202Z'%20fill='black'/%3e%3cpath%20d='M9.50794%205.48601H4.93594C4.81594%205.48601%204.44394%205.48601%204.44394%205.03101C4.44394%204.57601%204.81594%204.57501%204.93594%204.57501H15.0759C15.1959%204.57501%2015.5799%204.57501%2015.5799%205.03101C15.5799%205.48701%2015.2079%205.48601%2015.0759%205.48601H10.4559V6.67401H13.1799C14.0919%206.67401%2014.4999%206.97401%2014.4999%207.99401V11.222H15.1479C15.2919%2011.222%2015.6399%2011.234%2015.6399%2011.678C15.6399%2012.086%2015.3639%2012.133%2015.1479%2012.133H14.4999V13.921C14.4999%2015.205%2013.9359%2015.205%2012.5079%2015.205C12.3279%2015.205%2011.7999%2015.205%2011.6559%2015.182C11.3199%2015.146%2011.2599%2014.81%2011.2599%2014.666C11.2599%2014.198%2011.6199%2014.198%2011.8119%2014.198C11.9799%2014.198%2012.8799%2014.222%2012.9039%2014.222C13.2279%2014.222%2013.5159%2014.174%2013.5159%2013.67V12.134H6.50794V14.822C6.50794%2014.966%206.50794%2015.314%206.01594%2015.314C5.54794%2015.314%205.52394%2015.014%205.52394%2014.822V12.134H4.82794C4.70794%2012.134%204.33594%2012.134%204.33594%2011.679C4.33594%2011.319%204.57594%2011.223%204.82794%2011.223H5.52394V7.99501C5.52394%206.98701%205.91994%206.67501%206.84394%206.67501H9.50794V5.48601ZM9.50794%208.90601V7.52601H7.04794C6.69994%207.52601%206.50794%207.68201%206.50794%208.06701V8.90701L9.50794%208.90601ZM9.50794%209.72201H6.50794V11.222H9.50794V9.72201ZM10.4559%208.90601H13.5159V8.06601C13.5159%207.68201%2013.3239%207.52501%2012.9759%207.52501H10.4559V8.90501V8.90601ZM13.5159%209.72201H10.4559V11.222H13.5159V9.72201Z'%20fill='black'/%3e%3c/svg%3e"

def convertToTvkingdomArea(nhk_area):
	if nhk_area == "010":
		return "10"
	elif nhk_area == "011":
		return "11"
	elif nhk_area == "012":
		return "12"
	elif nhk_area == "013":
		return "13"
	elif nhk_area == "014":
		return "14"
	elif nhk_area == "015":
		return "15"
	elif nhk_area == "016":
		return "16"
	elif nhk_area == "040":
		return "17"
	elif nhk_area == "050":
		return "18"
	elif nhk_area == "060":
		return "19"
	elif nhk_area == "030":
		return "20"
	elif nhk_area == "070":
		return "21"
	elif nhk_area == "020":
		return "22"
	elif nhk_area == "130":
		return "23"
	elif nhk_area == "140":
		return "24"
	elif nhk_area == "100":
		return "25"
	elif nhk_area == "080":
		return "26"
	elif nhk_area == "120":
		return "27"
	elif nhk_area == "090":
		return "28"
	elif nhk_area == "110":
		return "29"
	elif nhk_area == "200":
		return "30"
	elif nhk_area == "150":
		return "31"
	elif nhk_area == "190":
		return "32"
	elif nhk_area == "230":
		return "33"
	elif nhk_area == "170":
		return "34"
	elif nhk_area == "220":
		return "35"
	elif nhk_area == "180":
		return "36"
	elif nhk_area == "160":
		return "37"
	elif nhk_area == "240":
		return "38"
	elif nhk_area == "210":
		return "39"
	elif nhk_area == "270":
		return "40"
	elif nhk_area == "260":
		return "41"
	elif nhk_area == "280":
		return "42"
	elif nhk_area == "300":
		return "43"
	elif nhk_area == "290":
		return "44"
	elif nhk_area == "250":
		return "45"
	elif nhk_area == "340":
		return "46"
	elif nhk_area == "330":
		return "47"
	elif nhk_area == "320":
		return "48"
	elif nhk_area == "310":
		return "49"
	elif nhk_area == "350":
		return "50"
	elif nhk_area == "380":
		return "51"
	elif nhk_area == "370":
		return "52"
	elif nhk_area == "360":
		return "53"
	elif nhk_area == "390":
		return "54"
	elif nhk_area == "400":
		return "55"
	elif nhk_area == "401":
		return "kk"
	elif nhk_area == "430":
		return "56"
	elif nhk_area == "420":
		return "57"
	elif nhk_area == "460":
		return "58"
	elif nhk_area == "450":
		return "59"
	elif nhk_area == "440":
		return "60"
	elif nhk_area == "410":
		return "61"
	elif nhk_area == "470":
		return "62"

def checkContent(html, year, month, day, area):
	if not "href=\"https://www.nhk.jp/timetable/" + area + "/\"" in html or not year + "年" + month + "月" + day + "日に" in html:
		print(year + "_" + month + "_" + day + "_NHK" + area + ".htmlの内容が間違っています")	

def getTargetPrograms(nhk_area):
	area = convertToTvkingdomArea(nhk_area)
	result = ["", "", "", "", "", "", "", "" ,"" ,"" ,"" ,""]
	if not "sG"+area in util.already and not area in ["24","27","29"]:
		result[1] = "sG"+area
		util.already.add("sG"+area)
	if not "sE"+area in util.already and not area in ["24","25","26","27","28","29","38","39","41","42","43","44","45"]:
		result[3] = "sE"+area
		util.already.add("sE"+area)
	if not "NB2" in util.already:
		result[5] = "NB2"
		util.already.add("NB2")
	return result

def extractTodays(html):
	splited = html.split("現在の時刻")
	if len(splited) == 1:
		return ""
	return splited[1]

# extractTodaysで切り分けたhtmlを与える
def extractItems(html):
	splited = html.split("class=\"program-table-td")
	splited.pop(0)
	return splited

# extractItemsで切り分けた配列htmlsを与える
# idx 1...総合サブ 3...教育サブ 5...BSサブ
def extractItemsByChannel(htmls, idx):
	result = []
	for html in htmls:
		if " / " + str((idx+1)*2) + " / span " in html:
			result.append(html)
	return result

# extractItemsByChannelで切り分けたhtmlを与える
def getInterval(html):
	splited = html.split(" / span ")
	return (int)(splited[1])

# extractItemsByChannelで切り分けたhtmlを与える
def extractStartTime(html):
	splited = html.split("style=\"grid-area: ")
	splited2 = splited[1].split(" / ")
	rowspan = (int)(splited2[0])

	splited = html.split("class=\"time-td\">")
	if len(splited) == 1:
		return ""
	splited2 = splited[1].split("<")
	splited3 = splited2[0].replace("午前","").replace("午後","").strip()
	start_hour = splited3.split(":")[0]
	start_minute = splited3.split(":")[1]
	if "午後" in splited2[0]:
		start_hour = str((int)(start_hour) + 12)
	elif rowspan >= 1186 and "午前" in splited2[0]:
		start_hour = str((int)(start_hour) + 24)
	elif len(start_hour) == 1:
		start_hour = "0" + start_hour
	return start_hour + start_minute

# extractItemsByChannelで切り分けたhtmlを与える
def extractTitle(html):
	splited1 = html.split("class=\"to-dtl\" href=\"javascript:void(0);\">")
	if len(splited1) == 1:
		return ""
	else:
		splited2 = splited1[1].split("</a>")
		result = splited2[0].replace("［新］","").replace("［終］","")
		return util.sanitize(result)

# extractItemsByChannelで切り分けたhtmlを与える
def extractDescription(html):
	splited1 = html.split("class=\"arrow\">")
	if len(splited1) == 1:
		return ""
	else:
		splited2 = splited1[1].split("</div>")
		return util.sanitize(splited2[0])

# extractItemsByChannelで切り分けたhtmlを与える
def extractIcons(html):
	types = []
	if IMG_COMMENT in html:
		types.append(util.append_type_name("解"))
	if IMG_STEREO in html:
		types.append(util.append_type_name("S"))
	if IMG_SS in html:
		types.append(util.append_type_name("SS"))
	if IMG_BILINGUAL in html:
		types.append(util.append_type_name("二"))
	if IMG_MULTISOUND in html:
		types.append(util.append_type_name("多"))
	if IMG_SUB in html:
		types.append(util.append_type_name("字"))
	if IMG_SIGN in html:
		types.append(util.append_type_name("手"))
	if IMG_DATA in html:
		types.append(util.append_type_name("デ"))
	if IMG_INTER in html:
		types.append(util.append_type_name("双"))
	if IMG_RE in html:
		types.append(util.append_type_name("再"))
	if "［新］" in html:
		types.append(util.append_type_name("新"))
	if "［終］" in html:
		types.append(util.append_type_name("終"))
	return types

def get_first_time(station_tag):
	if station_tag.startswith("sG"):
		return util.time_decode_base60(util.standard_programs_timeline[station_tag[1:]][0])
	elif station_tag.startswith("sE"):
		return util.time_decode_base60(util.standard_programs_timeline[station_tag[1:]][0])
	elif station_tag == "NB2":
		return util.time_decode_base60(util.standard_programs_timeline["BS1"][0])




def getCategoryCode(title_name):
	if "まるっと!" in title_name or "ゆう6かがわ" in title_name or "ロクいち!福岡" in title_name or "ニュースブリッジ北九州" in title_name or "イブニング長崎" in title_name or "情報WAVEかごしま" in title_name or "いろどりOITA" in title_name or "おきなわHOTeye" in title_name:
		return "100109"
	elif "ニュース" in title_name or "記者会見" in title_name:
		if "ワールド" in title_name or "CNN" in title_name or "世界" in title_name:
			return "100105"
		else:
			return "100100"
	elif "サタデーウオッチ" in title_name:
		return "100100"
	elif "戦没者追悼式" in title_name:
		return "100102"
	elif "マーケット" in title_name:
		return "100104"
	elif "オリンピック" in title_name or "パラリンピック" in title_name or "クライミングワールドカップ" in title_name:
		return "101106"
	elif "MLB" in title_name or "野球" in title_name:
		return "101101"
	elif "Jリーグ" in title_name or "WEリーグ" in title_name or "サッカー" in title_name or "JFA" in title_name or "FIFA" in title_name:
		return "101102"
	elif "ゴルフ" in title_name:
		return "101103"
	elif "Bリーグ" in title_name or "B2リーグ" in title_name or "Vリーグ" in title_name or "Wリーグ" in title_name or "熱血バスケ" in title_name or "バスケットボール" in title_name or "ラグビー" in title_name or "テニス" in title_name or "ウィンブルドン" in title_name or "卓球" in title_name or "ハンドボール" in title_name or "バレーボール" in title_name or "フットボール" in title_name or "甲子園ボウル" in title_name or "Nitto" in title_name:
		return "101104"
	elif  "相撲" in title_name or "剣道" in title_name or "柔道" in title_name or "空手道" in title_name:
		return "101105"
	elif "競泳" in title_name or "陸上" in title_name or "駅伝" in title_name:
		return "101107"
	elif "ノルディック" in title_name or "アルペン" in title_name or "カーリング" in title_name or "アイスホッケー" in title_name or "スピードスケート" in title_name or "スノーボード" in title_name or "NHK杯フィギュア" in title_name or "NHK杯ジャンプ" in title_name:
		return "101109"
	elif "ジャンプ" in title_name and "ワールドカップ" in title_name:
		return "101109"
	elif "競馬" in title_name:
		return "101110"
	elif "体操" in title_name or "クライミング" in title_name or "ローイング選手権" in title_name:
		return "101115"
	elif title_name == "あの人の極上ハンバーグ":
		return "102105"
	elif "スタジオパーク" in title_name or title_name == "土スタ":
		return "102107"
	elif "連続テレビ小説" in title_name:
		return "103100"
	elif "名曲アルバム" in title_name:
		return "104102"
	elif "みんなのうた" in title_name:
		return "104109"
	elif "せかほし" in title_name:
		return "105105"
	elif "天才てれびくん" in title_name:
		return "105115"
	elif "アニ×パラ" in title_name:
		return "107100"
	elif "美景" in title_name or "トラムの旅" in title_name or "世界遺産" in title_name or "大空撮" in title_name or "大縦走" in title_name or "天空の塩田" in title_name or "古代中国" in title_name or "空旅中国" in title_name or title_name == "京都 音めぐり" or title_name == "青海チベット鉄道" or "カラーでよみがえる" in title_name or "音紀行" in title_name or "映像詩" in title_name or "地球でイチバン" in title_name or "ドローン大航海" in title_name or "ゆかりの地を行く" in title_name or "行くぞ!最果て!" in title_name:
		return "108101"
	elif "動物" in title_name or "生きもの" in title_name or "小笠原" in title_name or "北アルプス" in title_name or "空中散歩" in title_name or "名峰" in title_name or "にっぽん百名山" in title_name or "巨樹の旅" in title_name or "ふるさとの絶景" in title_name or title_name == "ごろごろパンダ日記" or "グレートネイチャー" in title_name:
		return "108102"
	elif "クルージング" in title_name:
		return "110100"
	elif "美の壺" in title_name:
		return "110102"
	elif "高校講座" in title_name or title_name == "ロンリのちから":
		return "110109"
	elif title_name == "ＮＨＫラーニング":
		return "110111"
	else:
		return "115115"

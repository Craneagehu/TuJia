from selenium import webdriver
import pandas as pd


url = "https://www.tujia.com/unitlist?startDate=2020-02-20&endDate=2020-02-21&cds=1_752_%25E9%2587%2591%25E4%25B8%259C%25E5%258C%25BA&cityId=113&ssr=off"
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(20)
# 编写修改navigator.webdriver值的JavaScript代码
script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
# 运行JavaScript代码
driver.execute_script(script)
names_1 = []
names_2 = []
prices_1 = []
prices_2 = []
while True:
    #items = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="unitList-container"]/div/div')))
    items = driver.find_elements_by_xpath('//*[@id="unitList-container"]/div/div')
    # //*[@id="unitList-container"]/div/div[1]/div[2]/div[1]/h3/a
    # //*[@id="unitList-container"]/div/div[1]/div[2]/div[2]/div[1]/a/span[1]
    # //*[@id="unitList-container"]/div/div[22]/div[2]/div[2]/div[1]/a/span[1]
    for item in items:
        name = item.find_element_by_xpath('.//div[2]/div[1]/h3/a').text
        try:
            price = item.find_element_by_xpath('.//div[2]/div[2]/div[1]/a/span[1]').text
        except Exception as e:
            price = ''
        isorder = item.find_element_by_xpath('.//div[1]/div[1]').get_attribute('class')
        if isorder == "label-tag":
            names_1.append(name)
            prices_1.append(price)
            print(name,price,isorder)
        else:
            names_2.append(name)
            prices_2.append(price)
            print(name, price, isorder)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        next_page = driver.find_element_by_css_selector('.pagination ul li[page-rel=nextpage]')

        if next_page.text:
            next_page.click()
            driver.implicitly_wait(20)
    except:
        break
driver.quit()
print(names_1)
print(len(names_1),len(prices_1),len(names_2),len(prices_2))


writer = pd.ExcelWriter('output.xlsx')
df1 = pd.DataFrame(data={'no_order':names_1,'price_1':prices_1})
df2 = pd.DataFrame(data={'ordered':names_2,'price_2':prices_2})
df1.to_excel(writer,'sheet1',index=False)   # shee1 为工作表名
df2.to_excel(writer,'sheet2',index=False)
writer.save()


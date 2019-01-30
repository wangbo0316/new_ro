import xlrd


class ExcelLoader:

    def __init__(self,pathName,sheet_name):
        self.workBook = xlrd.open_workbook(pathName)
        try:
            self.sheet = self.workBook.sheet_by_name(sheet_name)
        except:
            self.sheet = self.workBook.sheet_by_index(sheet_name)
        self.row_size = len(self.sheet.col_values(0))
        self.col_size = len(self.sheet.row_values(0))
        pass

    def row_values(self,rowx,start_colx=0,end_colx=None):
        return self.sheet.row_values(rowx,start_colx,end_colx)

    def col_values(self,colx,start_rowx=0,end_rowx=None):
        return self.sheet.col_values(colx,start_rowx,end_rowx)

    def get_area(self,row_area,col_area):
        area = []
        for row_i in range(row_area[0],row_area[1]+1):
            row = self.sheet.row_values(row_i,col_area[0],col_area[1]+1)
            area.append(row)
        return area





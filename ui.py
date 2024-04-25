# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'KaomojiHelperosWMFt.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFontComboBox,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QKeySequenceEdit, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QTabWidget, QTableView,
    QToolButton, QVBoxLayout, QWidget)
import resources

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 400)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.MainVerticalLayout = QVBoxLayout()
        self.MainVerticalLayout.setSpacing(6)
        self.MainVerticalLayout.setObjectName(u"MainVerticalLayout")
        self.SearchLineEdit = QLineEdit(Form)
        self.SearchLineEdit.setObjectName(u"SearchLineEdit")

        self.MainVerticalLayout.addWidget(self.SearchLineEdit)

        self.TabsWidget = QTabWidget(Form)
        self.TabsWidget.setObjectName(u"TabsWidget")
        self.TabsWidget.setAutoFillBackground(False)
        self.TabsWidget.setStyleSheet(u"QTabWidget::tab-bar {\n"
"	alignment: center;\n"
"}")
        self.TabsWidget.setTabPosition(QTabWidget.North)
        self.TabsWidget.setTabShape(QTabWidget.Rounded)
        self.SearchTab = QWidget()
        self.SearchTab.setObjectName(u"SearchTab")
        self.verticalLayout_8 = QVBoxLayout(self.SearchTab)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.SearchVerticalLayout = QVBoxLayout()
        self.SearchVerticalLayout.setObjectName(u"SearchVerticalLayout")
        self.SearchTableView = QTableView(self.SearchTab)
        self.SearchTableView.setObjectName(u"SearchTableView")

        self.SearchVerticalLayout.addWidget(self.SearchTableView)


        self.verticalLayout_8.addLayout(self.SearchVerticalLayout)

        self.SearchHorizontalLayout = QHBoxLayout()
        self.SearchHorizontalLayout.setSpacing(8)
        self.SearchHorizontalLayout.setObjectName(u"SearchHorizontalLayout")
        self.SearchFirstButton = QPushButton(self.SearchTab)
        self.SearchFirstButton.setObjectName(u"SearchFirstButton")
        icon = QIcon()
        icon.addFile(u":/first/first.png", QSize(), QIcon.Normal, QIcon.Off)
        self.SearchFirstButton.setIcon(icon)
        self.SearchFirstButton.setIconSize(QSize(16, 16))

        self.SearchHorizontalLayout.addWidget(self.SearchFirstButton)

        self.SearchPreviousButton = QPushButton(self.SearchTab)
        self.SearchPreviousButton.setObjectName(u"SearchPreviousButton")
        icon1 = QIcon()
        icon1.addFile(u":/previous/previous.png", QSize(), QIcon.Normal, QIcon.Off)
        self.SearchPreviousButton.setIcon(icon1)

        self.SearchHorizontalLayout.addWidget(self.SearchPreviousButton)

        self.SearchStatusLabel = QLabel(self.SearchTab)
        self.SearchStatusLabel.setObjectName(u"SearchStatusLabel")
        self.SearchStatusLabel.setMinimumSize(QSize(180, 24))
        self.SearchStatusLabel.setAlignment(Qt.AlignCenter)

        self.SearchHorizontalLayout.addWidget(self.SearchStatusLabel)

        self.SearchNextButton = QPushButton(self.SearchTab)
        self.SearchNextButton.setObjectName(u"SearchNextButton")
        icon2 = QIcon()
        icon2.addFile(u":/next/next.png", QSize(), QIcon.Normal, QIcon.Off)
        self.SearchNextButton.setIcon(icon2)

        self.SearchHorizontalLayout.addWidget(self.SearchNextButton)

        self.SearchLastButton = QPushButton(self.SearchTab)
        self.SearchLastButton.setObjectName(u"SearchLastButton")
        icon3 = QIcon()
        icon3.addFile(u":/last/last.png", QSize(), QIcon.Normal, QIcon.Off)
        self.SearchLastButton.setIcon(icon3)

        self.SearchHorizontalLayout.addWidget(self.SearchLastButton)


        self.verticalLayout_8.addLayout(self.SearchHorizontalLayout)

        icon4 = QIcon()
        icon4.addFile(u":/search/search.png", QSize(), QIcon.Normal, QIcon.Off)
        self.TabsWidget.addTab(self.SearchTab, icon4, "")
        self.RecentlyUsedTab = QWidget()
        self.RecentlyUsedTab.setObjectName(u"RecentlyUsedTab")
        self.verticalLayout_6 = QVBoxLayout(self.RecentlyUsedTab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.RecentlyUsedVerticalLayout = QVBoxLayout()
        self.RecentlyUsedVerticalLayout.setObjectName(u"RecentlyUsedVerticalLayout")
        self.RecentlyUsedTableView = QTableView(self.RecentlyUsedTab)
        self.RecentlyUsedTableView.setObjectName(u"RecentlyUsedTableView")

        self.RecentlyUsedVerticalLayout.addWidget(self.RecentlyUsedTableView)


        self.verticalLayout_6.addLayout(self.RecentlyUsedVerticalLayout)

        self.RecentlyUsedHorizontalLayout = QHBoxLayout()
        self.RecentlyUsedHorizontalLayout.setSpacing(8)
        self.RecentlyUsedHorizontalLayout.setObjectName(u"RecentlyUsedHorizontalLayout")
        self.RecentlyUsedFirstButton = QPushButton(self.RecentlyUsedTab)
        self.RecentlyUsedFirstButton.setObjectName(u"RecentlyUsedFirstButton")
        self.RecentlyUsedFirstButton.setIcon(icon)

        self.RecentlyUsedHorizontalLayout.addWidget(self.RecentlyUsedFirstButton)

        self.RecentlyUsedPreviousButton = QPushButton(self.RecentlyUsedTab)
        self.RecentlyUsedPreviousButton.setObjectName(u"RecentlyUsedPreviousButton")
        self.RecentlyUsedPreviousButton.setIcon(icon1)

        self.RecentlyUsedHorizontalLayout.addWidget(self.RecentlyUsedPreviousButton)

        self.RecentlyUsedStatusLabel = QLabel(self.RecentlyUsedTab)
        self.RecentlyUsedStatusLabel.setObjectName(u"RecentlyUsedStatusLabel")
        self.RecentlyUsedStatusLabel.setMinimumSize(QSize(180, 24))
        self.RecentlyUsedStatusLabel.setAlignment(Qt.AlignCenter)

        self.RecentlyUsedHorizontalLayout.addWidget(self.RecentlyUsedStatusLabel)

        self.RecentlyUsedNextButton = QPushButton(self.RecentlyUsedTab)
        self.RecentlyUsedNextButton.setObjectName(u"RecentlyUsedNextButton")
        self.RecentlyUsedNextButton.setIcon(icon2)

        self.RecentlyUsedHorizontalLayout.addWidget(self.RecentlyUsedNextButton)

        self.RecentlyUsedLastButton = QPushButton(self.RecentlyUsedTab)
        self.RecentlyUsedLastButton.setObjectName(u"RecentlyUsedLastButton")
        self.RecentlyUsedLastButton.setIcon(icon3)

        self.RecentlyUsedHorizontalLayout.addWidget(self.RecentlyUsedLastButton)


        self.verticalLayout_6.addLayout(self.RecentlyUsedHorizontalLayout)

        icon5 = QIcon()
        icon5.addFile(u":/recent/recent.png", QSize(), QIcon.Normal, QIcon.Off)
        self.TabsWidget.addTab(self.RecentlyUsedTab, icon5, "")
        self.FavoritesTab = QWidget()
        self.FavoritesTab.setObjectName(u"FavoritesTab")
        self.verticalLayout_4 = QVBoxLayout(self.FavoritesTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.FavoritesVerticalLayout = QVBoxLayout()
        self.FavoritesVerticalLayout.setObjectName(u"FavoritesVerticalLayout")
        self.FavoritesTableView = QTableView(self.FavoritesTab)
        self.FavoritesTableView.setObjectName(u"FavoritesTableView")

        self.FavoritesVerticalLayout.addWidget(self.FavoritesTableView)


        self.verticalLayout_4.addLayout(self.FavoritesVerticalLayout)

        self.FavoritesHorizontalLayout = QHBoxLayout()
        self.FavoritesHorizontalLayout.setSpacing(8)
        self.FavoritesHorizontalLayout.setObjectName(u"FavoritesHorizontalLayout")
        self.FavoritesFirstButton = QPushButton(self.FavoritesTab)
        self.FavoritesFirstButton.setObjectName(u"FavoritesFirstButton")
        self.FavoritesFirstButton.setIcon(icon)

        self.FavoritesHorizontalLayout.addWidget(self.FavoritesFirstButton)

        self.FavoritesPreviousButton = QPushButton(self.FavoritesTab)
        self.FavoritesPreviousButton.setObjectName(u"FavoritesPreviousButton")
        self.FavoritesPreviousButton.setIcon(icon1)

        self.FavoritesHorizontalLayout.addWidget(self.FavoritesPreviousButton)

        self.FavoritesStatusLabel = QLabel(self.FavoritesTab)
        self.FavoritesStatusLabel.setObjectName(u"FavoritesStatusLabel")
        self.FavoritesStatusLabel.setMinimumSize(QSize(180, 24))
        self.FavoritesStatusLabel.setAlignment(Qt.AlignCenter)

        self.FavoritesHorizontalLayout.addWidget(self.FavoritesStatusLabel)

        self.FavoritesNextButton = QPushButton(self.FavoritesTab)
        self.FavoritesNextButton.setObjectName(u"FavoritesNextButton")
        self.FavoritesNextButton.setIcon(icon2)

        self.FavoritesHorizontalLayout.addWidget(self.FavoritesNextButton)

        self.FavoritesLastButton = QPushButton(self.FavoritesTab)
        self.FavoritesLastButton.setObjectName(u"FavoritesLastButton")
        self.FavoritesLastButton.setIcon(icon3)

        self.FavoritesHorizontalLayout.addWidget(self.FavoritesLastButton)


        self.verticalLayout_4.addLayout(self.FavoritesHorizontalLayout)

        icon6 = QIcon()
        icon6.addFile(u":/favorite/favorite.png", QSize(), QIcon.Normal, QIcon.Off)
        self.TabsWidget.addTab(self.FavoritesTab, icon6, "")
        self.SettingsTab = QWidget()
        self.SettingsTab.setObjectName(u"SettingsTab")
        self.verticalLayout_9 = QVBoxLayout(self.SettingsTab)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.SettingsScrollArea = QScrollArea(self.SettingsTab)
        self.SettingsScrollArea.setObjectName(u"SettingsScrollArea")
        self.SettingsScrollArea.setFrameShadow(QFrame.Sunken)
        self.SettingsScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 537, 533))
        self.verticalLayout_14 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.GeneralGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.GeneralGroupBox.setObjectName(u"GeneralGroupBox")
        self.verticalLayout_12 = QVBoxLayout(self.GeneralGroupBox)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.KaomojiSetHorizontalLayout = QHBoxLayout()
        self.KaomojiSetHorizontalLayout.setObjectName(u"KaomojiSetHorizontalLayout")
        self.KaomojiSetLabel = QLabel(self.GeneralGroupBox)
        self.KaomojiSetLabel.setObjectName(u"KaomojiSetLabel")

        self.KaomojiSetHorizontalLayout.addWidget(self.KaomojiSetLabel)

        self.KaomojiSetLineEdit = QLineEdit(self.GeneralGroupBox)
        self.KaomojiSetLineEdit.setObjectName(u"KaomojiSetLineEdit")
        self.KaomojiSetLineEdit.setReadOnly(True)

        self.KaomojiSetHorizontalLayout.addWidget(self.KaomojiSetLineEdit)

        self.KaomojiSetButton = QToolButton(self.GeneralGroupBox)
        self.KaomojiSetButton.setObjectName(u"KaomojiSetButton")

        self.KaomojiSetHorizontalLayout.addWidget(self.KaomojiSetButton)


        self.verticalLayout_12.addLayout(self.KaomojiSetHorizontalLayout)

        self.DefaultTabHorizontalLayout = QHBoxLayout()
        self.DefaultTabHorizontalLayout.setObjectName(u"DefaultTabHorizontalLayout")
        self.DefaultTabLabel = QLabel(self.GeneralGroupBox)
        self.DefaultTabLabel.setObjectName(u"DefaultTabLabel")

        self.DefaultTabHorizontalLayout.addWidget(self.DefaultTabLabel)

        self.DefaultTabComboBox = QComboBox(self.GeneralGroupBox)
        self.DefaultTabComboBox.setObjectName(u"DefaultTabComboBox")

        self.DefaultTabHorizontalLayout.addWidget(self.DefaultTabComboBox)


        self.verticalLayout_12.addLayout(self.DefaultTabHorizontalLayout)

        self.LaunchAtStartupCheckbox = QCheckBox(self.GeneralGroupBox)
        self.LaunchAtStartupCheckbox.setObjectName(u"LaunchAtStartupCheckbox")

        self.verticalLayout_12.addWidget(self.LaunchAtStartupCheckbox)

        self.ClearSearchEntryCheckbox = QCheckBox(self.GeneralGroupBox)
        self.ClearSearchEntryCheckbox.setObjectName(u"ClearSearchEntryCheckbox")

        self.verticalLayout_12.addWidget(self.ClearSearchEntryCheckbox)


        self.verticalLayout_14.addWidget(self.GeneralGroupBox)

        self.AppearanceGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.AppearanceGroupBox.setObjectName(u"AppearanceGroupBox")
        self.verticalLayout_11 = QVBoxLayout(self.AppearanceGroupBox)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.ThemeHorizontalLayout = QHBoxLayout()
        self.ThemeHorizontalLayout.setObjectName(u"ThemeHorizontalLayout")
        self.ThemeLabel = QLabel(self.AppearanceGroupBox)
        self.ThemeLabel.setObjectName(u"ThemeLabel")

        self.ThemeHorizontalLayout.addWidget(self.ThemeLabel)

        self.ThemeComboBox = QComboBox(self.AppearanceGroupBox)
        self.ThemeComboBox.setObjectName(u"ThemeComboBox")

        self.ThemeHorizontalLayout.addWidget(self.ThemeComboBox)


        self.verticalLayout_11.addLayout(self.ThemeHorizontalLayout)

        self.FontHorizontalLayout = QHBoxLayout()
        self.FontHorizontalLayout.setObjectName(u"FontHorizontalLayout")
        self.FontLabel = QLabel(self.AppearanceGroupBox)
        self.FontLabel.setObjectName(u"FontLabel")

        self.FontHorizontalLayout.addWidget(self.FontLabel)

        self.FontComboBox = QFontComboBox(self.AppearanceGroupBox)
        self.FontComboBox.setObjectName(u"FontComboBox")

        self.FontHorizontalLayout.addWidget(self.FontComboBox)


        self.verticalLayout_11.addLayout(self.FontHorizontalLayout)

        self.FontColorHorizontalLayout = QHBoxLayout()
        self.FontColorHorizontalLayout.setObjectName(u"FontColorHorizontalLayout")
        self.FontColorLabel = QLabel(self.AppearanceGroupBox)
        self.FontColorLabel.setObjectName(u"FontColorLabel")

        self.FontColorHorizontalLayout.addWidget(self.FontColorLabel)

        self.FontColorButton = QPushButton(self.AppearanceGroupBox)
        self.FontColorButton.setObjectName(u"FontColorButton")

        self.FontColorHorizontalLayout.addWidget(self.FontColorButton)


        self.verticalLayout_11.addLayout(self.FontColorHorizontalLayout)


        self.verticalLayout_14.addWidget(self.AppearanceGroupBox)

        self.MiscellaneousGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.MiscellaneousGroupBox.setObjectName(u"MiscellaneousGroupBox")
        self.verticalLayout_13 = QVBoxLayout(self.MiscellaneousGroupBox)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.ShowSoundHorizontalLayout = QHBoxLayout()
        self.ShowSoundHorizontalLayout.setObjectName(u"ShowSoundHorizontalLayout")
        self.ShowSoundLabel = QLabel(self.MiscellaneousGroupBox)
        self.ShowSoundLabel.setObjectName(u"ShowSoundLabel")
        self.ShowSoundLabel.setMinimumSize(QSize(74, 0))

        self.ShowSoundHorizontalLayout.addWidget(self.ShowSoundLabel)

        self.ShowSoundLineEdit = QLineEdit(self.MiscellaneousGroupBox)
        self.ShowSoundLineEdit.setObjectName(u"ShowSoundLineEdit")
        self.ShowSoundLineEdit.setReadOnly(True)

        self.ShowSoundHorizontalLayout.addWidget(self.ShowSoundLineEdit)

        self.ShowSoundButton = QToolButton(self.MiscellaneousGroupBox)
        self.ShowSoundButton.setObjectName(u"ShowSoundButton")

        self.ShowSoundHorizontalLayout.addWidget(self.ShowSoundButton)


        self.verticalLayout_13.addLayout(self.ShowSoundHorizontalLayout)

        self.HideSoundHorizontalLayout = QHBoxLayout()
        self.HideSoundHorizontalLayout.setObjectName(u"HideSoundHorizontalLayout")
        self.HideSoundLabel = QLabel(self.MiscellaneousGroupBox)
        self.HideSoundLabel.setObjectName(u"HideSoundLabel")
        self.HideSoundLabel.setMinimumSize(QSize(74, 0))

        self.HideSoundHorizontalLayout.addWidget(self.HideSoundLabel)

        self.HideSoundLineEdit = QLineEdit(self.MiscellaneousGroupBox)
        self.HideSoundLineEdit.setObjectName(u"HideSoundLineEdit")
        self.HideSoundLineEdit.setReadOnly(True)

        self.HideSoundHorizontalLayout.addWidget(self.HideSoundLineEdit)

        self.HideSoundButton = QToolButton(self.MiscellaneousGroupBox)
        self.HideSoundButton.setObjectName(u"HideSoundButton")

        self.HideSoundHorizontalLayout.addWidget(self.HideSoundButton)


        self.verticalLayout_13.addLayout(self.HideSoundHorizontalLayout)


        self.verticalLayout_14.addWidget(self.MiscellaneousGroupBox)

        self.KeybindsGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.KeybindsGroupBox.setObjectName(u"KeybindsGroupBox")
        self.verticalLayout_10 = QVBoxLayout(self.KeybindsGroupBox)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.ShowWindowHorizontalLayout = QHBoxLayout()
        self.ShowWindowHorizontalLayout.setObjectName(u"ShowWindowHorizontalLayout")
        self.ShowWindowLabel = QLabel(self.KeybindsGroupBox)
        self.ShowWindowLabel.setObjectName(u"ShowWindowLabel")
        self.ShowWindowLabel.setMinimumSize(QSize(74, 0))

        self.ShowWindowHorizontalLayout.addWidget(self.ShowWindowLabel)

        self.ShowWindowKeySequence = QKeySequenceEdit(self.KeybindsGroupBox)
        self.ShowWindowKeySequence.setObjectName(u"ShowWindowKeySequence")

        self.ShowWindowHorizontalLayout.addWidget(self.ShowWindowKeySequence)


        self.verticalLayout_10.addLayout(self.ShowWindowHorizontalLayout)

        self.HideWindowHorizontalLayout = QHBoxLayout()
        self.HideWindowHorizontalLayout.setObjectName(u"HideWindowHorizontalLayout")
        self.HideWindowLabel = QLabel(self.KeybindsGroupBox)
        self.HideWindowLabel.setObjectName(u"HideWindowLabel")
        self.HideWindowLabel.setMinimumSize(QSize(74, 0))

        self.HideWindowHorizontalLayout.addWidget(self.HideWindowLabel)

        self.HideWindowKeySequence = QKeySequenceEdit(self.KeybindsGroupBox)
        self.HideWindowKeySequence.setObjectName(u"HideWindowKeySequence")

        self.HideWindowHorizontalLayout.addWidget(self.HideWindowKeySequence)


        self.verticalLayout_10.addLayout(self.HideWindowHorizontalLayout)

        self.PreviousPageHorizontalLayout = QHBoxLayout()
        self.PreviousPageHorizontalLayout.setObjectName(u"PreviousPageHorizontalLayout")
        self.PreviousPageLabel = QLabel(self.KeybindsGroupBox)
        self.PreviousPageLabel.setObjectName(u"PreviousPageLabel")
        self.PreviousPageLabel.setMinimumSize(QSize(74, 0))

        self.PreviousPageHorizontalLayout.addWidget(self.PreviousPageLabel)

        self.PreviousPageKeySequence = QKeySequenceEdit(self.KeybindsGroupBox)
        self.PreviousPageKeySequence.setObjectName(u"PreviousPageKeySequence")

        self.PreviousPageHorizontalLayout.addWidget(self.PreviousPageKeySequence)


        self.verticalLayout_10.addLayout(self.PreviousPageHorizontalLayout)

        self.NextPageHorizontalLayout = QHBoxLayout()
        self.NextPageHorizontalLayout.setObjectName(u"NextPageHorizontalLayout")
        self.NextPageLabel = QLabel(self.KeybindsGroupBox)
        self.NextPageLabel.setObjectName(u"NextPageLabel")
        self.NextPageLabel.setMinimumSize(QSize(74, 0))

        self.NextPageHorizontalLayout.addWidget(self.NextPageLabel)

        self.NextPageKeySequence = QKeySequenceEdit(self.KeybindsGroupBox)
        self.NextPageKeySequence.setObjectName(u"NextPageKeySequence")

        self.NextPageHorizontalLayout.addWidget(self.NextPageKeySequence)


        self.verticalLayout_10.addLayout(self.NextPageHorizontalLayout)


        self.verticalLayout_14.addWidget(self.KeybindsGroupBox)

        self.SettingsScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_9.addWidget(self.SettingsScrollArea)

        icon7 = QIcon()
        icon7.addFile(u":/settings/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.TabsWidget.addTab(self.SettingsTab, icon7, "")

        self.MainVerticalLayout.addWidget(self.TabsWidget)


        self.verticalLayout_2.addLayout(self.MainVerticalLayout)


        self.retranslateUi(Form)

        self.TabsWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"KaomojiHelper", None))
        self.SearchLineEdit.setText("")
        self.SearchLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Search a kaomoji...", None))
        self.SearchFirstButton.setText("")
        self.SearchPreviousButton.setText("")
        self.SearchStatusLabel.setText(QCoreApplication.translate("Form", u"0-0 results | 0 (total)", None))
        self.SearchNextButton.setText("")
        self.SearchLastButton.setText("")
        self.TabsWidget.setTabText(self.TabsWidget.indexOf(self.SearchTab), QCoreApplication.translate("Form", u"Search", None))
        self.RecentlyUsedFirstButton.setText("")
        self.RecentlyUsedPreviousButton.setText("")
        self.RecentlyUsedStatusLabel.setText(QCoreApplication.translate("Form", u"0-0 results | 0 (total)", None))
        self.RecentlyUsedNextButton.setText("")
        self.RecentlyUsedLastButton.setText("")
        self.TabsWidget.setTabText(self.TabsWidget.indexOf(self.RecentlyUsedTab), QCoreApplication.translate("Form", u"Recently used", None))
        self.FavoritesFirstButton.setText("")
        self.FavoritesPreviousButton.setText("")
        self.FavoritesStatusLabel.setText(QCoreApplication.translate("Form", u"0-0 results | 0 (total)", None))
        self.FavoritesNextButton.setText("")
        self.FavoritesLastButton.setText("")
        self.TabsWidget.setTabText(self.TabsWidget.indexOf(self.FavoritesTab), QCoreApplication.translate("Form", u"Favorites", None))
        self.GeneralGroupBox.setTitle(QCoreApplication.translate("Form", u"General", None))
        self.KaomojiSetLabel.setText(QCoreApplication.translate("Form", u"Kaomoji set", None))
        self.KaomojiSetButton.setText(QCoreApplication.translate("Form", u"...", None))
        self.DefaultTabLabel.setText(QCoreApplication.translate("Form", u"Default tab", None))
        self.LaunchAtStartupCheckbox.setText(QCoreApplication.translate("Form", u"Launch at startup", None))
        self.ClearSearchEntryCheckbox.setText(QCoreApplication.translate("Form", u"Clear search entry upon clicking on a kaomoji", None))
        self.AppearanceGroupBox.setTitle(QCoreApplication.translate("Form", u"Appearance", None))
        self.ThemeLabel.setText(QCoreApplication.translate("Form", u"Theme", None))
        self.FontLabel.setText(QCoreApplication.translate("Form", u"Font", None))
        self.FontColorLabel.setText(QCoreApplication.translate("Form", u"Font color", None))
        self.FontColorButton.setText(QCoreApplication.translate("Form", u"Change color", None))
        self.MiscellaneousGroupBox.setTitle(QCoreApplication.translate("Form", u"Miscellaneous", None))
        self.ShowSoundLabel.setText(QCoreApplication.translate("Form", u"Show sound", None))
        self.ShowSoundButton.setText(QCoreApplication.translate("Form", u"...", None))
        self.HideSoundLabel.setText(QCoreApplication.translate("Form", u"Hide sound", None))
        self.HideSoundButton.setText(QCoreApplication.translate("Form", u"...", None))
        self.KeybindsGroupBox.setTitle(QCoreApplication.translate("Form", u"Keybinds", None))
        self.ShowWindowLabel.setText(QCoreApplication.translate("Form", u"Show window", None))
        self.HideWindowLabel.setText(QCoreApplication.translate("Form", u"Hide window", None))
        self.PreviousPageLabel.setText(QCoreApplication.translate("Form", u"Previous page", None))
        self.NextPageLabel.setText(QCoreApplication.translate("Form", u"Next page", None))
        self.TabsWidget.setTabText(self.TabsWidget.indexOf(self.SettingsTab), QCoreApplication.translate("Form", u"Settings", None))
    # retranslateUi


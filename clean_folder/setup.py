from setuptools import setup,find_namespace_packages

setup(name='clean_folder',
      version='0.0.1',
      description='Very useful code',
      url='https://github.com/MSRoma/clean_folder',
      author='Samchuk Roman',
      author_email='tesmai@i.ua',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts':['clean-folder=clean_folder.clean:run']}
)